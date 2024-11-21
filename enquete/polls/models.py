import datetime
from django.db import models
from django.db.models import Sum
from django.utils import timezone

# Create your models here.

class Pergunta(models.Model):
    texto_da_pergunta = models.CharField(max_length=200)
    data_publicacao = models.DateTimeField("Data Publicação")

    def __str__(self):
        return self.texto_da_pergunta
    
    def publicada_recentemente(self):
        now = timezone.now()
        # return self.data_publicacao >= timezone.now() - datetime.timedelta(days=2)
        return now - datetime.timedelta(days=2) <= self.data_publicacao <= now

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    texto_da_resposta = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto_da_resposta
    
    def totalVotos(self): 
        id_pergunta = self.pergunta.id
        pergunta = Pergunta.objects.get(id=id_pergunta)
        total_votos = Resposta.objects.filter(pergunta=id_pergunta).aggregate(Sum("votos")).get('votos__sum', 0.00)
        percentual = ((self.votos * 100) / total_votos)

        return percentual

