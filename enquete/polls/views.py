from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CadastraUsuarios, AlteraUsuarios, ProfileForm

from .models import Pergunta, Resposta, UserProfile


def registro(request):

    if request.method == "POST":

        usuario_form = CadastraUsuarios(request.POST)
        profile_form = ProfileForm(request.POST)

        if (usuario_form.is_valid() and profile_form.is_valid()):
            user = usuario_form.save()

            user.refresh_from_db()  # This will load the UserProfile created by the Signal
            user.userprofile.sexo = profile_form.cleaned_data.get('sexo')
            user.userprofile.data_nascimento = profile_form.cleaned_data.get('data_nascimento')
            user.save()

            senha = usuario_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=senha)
            login(request, user)

            nome = usuario_form.cleaned_data.get('first_name')            
            
            messages.success(request, f"Usuário {nome} cadastrado com sucesso!")   
            return redirect("polls:index")

        else:

            contextoErro = {
                'usuario_form':CadastraUsuarios(request.POST),
                'profile_form':ProfileForm(request.POST)
            }

            messages.warning(request, "Houve um problema ao Criar o Cadastro!")
            # return redirect("polls:Registro")
            return render(request, "polls/registro.html", contextoErro)
    
    else:

        contexto = {
            'usuario_form':CadastraUsuarios(),
            'profile_form':ProfileForm()
        }

        return render(request, "polls/registro.html", contexto)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("polls:index")
    else:
        form = AuthenticationForm()
    
    return render(request, "polls/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("polls:Login")

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "lista_ultimas_perguntas"

    def get_queryset(self):
        return Pergunta.objects.filter(data_publicacao__lte=timezone.now()).order_by("data_publicacao")[:5]
    
class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Pergunta
    template_name = "polls/detail.html"

@login_required
def vote(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)

    try:
        selecao = pergunta.resposta_set.get(pk=request.POST["escolha"])
    except (KeyError, Resposta.DoesNotExist):
        return render(request, "polls/detail.html",
                      {
                          "pergunta": pergunta,
                          "error_message": "Você não selecionou nenhuma Resposta"
                      }
                      )
    else:
        selecao.votos = F("votos") + 1
        selecao.save()

        return HttpResponseRedirect(reverse("polls:Resultados", args=(pergunta_id,)))

@login_required    
def teste(request):
    return render(request, "polls/teste.html")


# class ResultsView(LoginRequiredMixin, generic.DetailView):
#     model = Pergunta
#     template_name = "polls/resultado.html"

def ResultsView(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)

    return render(request, "polls/resultado.html", {"pergunta": pergunta})

@login_required
def altera_cadastro(request):
    
    if(request.method == "POST"):

        usuario_form = AlteraUsuarios(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)

        if(usuario_form.is_valid() and profile_form.is_valid()):
            nome = usuario_form.cleaned_data.get('first_name')

            usuario_form.save()
            profile_form.save()
            
            messages.success(request, f"{nome} seus dados foram atualizados com sucesso!")        
            return redirect("polls:index")
        
        else:

            messages.warning(request, "Houve um problema ao Alterar os dados!")
            return redirect("polls:AlteraCadastro")
        
    else:

        usuario_form = AlteraUsuarios(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)

        contexto = {
            "usuario_form": usuario_form,
            "profile_form": profile_form
        }

        return render(request, "polls/altera.html", contexto)