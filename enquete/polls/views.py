from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CadastraUsuarios, AlteraUsuarios

from .models import Pergunta, Resposta


def registro(request):
    if request.method == "POST":

        form = CadastraUsuarios(request.POST)
        if form.is_valid():
            nome = form.cleaned_data.get('first_name')
            login(request, form.save())
            messages.success(request, f"Usuário {nome} cadastrado com sucesso!")
            
            return redirect("polls:index")
    else:

        form = CadastraUsuarios()

    return render(request, "polls/registro.html", {"form": form})


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
        # return Pergunta.objects.order_by("data_publicacao")[:5]
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

        form = AlteraUsuarios(request.POST, instance=request.user)

        if(form.is_valid()):
            nome = form.cleaned_data.get('first_name')
            
            messages.success(request, f"{nome} seus dados foram atualizados com sucesso!")

            form.save()
        
        return redirect("polls:index")

    else:

        form = AlteraUsuarios(instance=request.user)

        return render(request, "polls/altera.html", {"form": form})
    