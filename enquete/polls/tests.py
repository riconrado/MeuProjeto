import datetime
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from . models import Pergunta, Resposta


class PerguntaModelTests(TestCase):
    def teste_foi_publicado_recentemente(self):
        time = timezone.now() + datetime.timedelta(days=30)
        data_futura = Pergunta(data_publicacao=time)
        self.assertIs(data_futura.publicada_recentemente(), False)

class PerguntaTesteData(TestCase):
    def teste(self):
        print((timezone.now() - datetime.timedelta(days=5)) <= timezone.now() <= (timezone.now() - datetime.timedelta(days=1)))

class UserCreationFormTest(TestCase):
    def test_form(self):
        data = {
            'username': 'ricardo',
            'password1': 'conrado123',
            'password2': 'conrado123',
        }

        form = UserCreationForm(data)

        self.assertTrue(form.is_valid())
        
class SomaValor(TestCase):
        def test_somaVotos(self):

            Pergunta.objects.create(texto_da_pergunta="O teste Funciona ?",data_publicacao= timezone.now())

            perg = Pergunta.objects.get(id=1)

            perg.resposta_set.create(texto_da_resposta="Sim",votos=40)
            perg.resposta_set.create(texto_da_resposta="Não",votos=60)

            resp = Resposta.objects.all()
            
            total_respostas = Resposta.objects.count()
            total_votos = Resposta.objects.aggregate(Sum("votos")).get('votos__sum', 0.00)
            perc_dict ={}

            for i in perg.resposta_set.all():
                  
                  perc = i.votos * 100 / 100
                  perc_dict.update({ i.id: perc })
            
            print(perc_dict)
            print(total_votos)