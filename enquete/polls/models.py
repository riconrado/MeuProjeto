import datetime
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User


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

class UserProfile(models.Model):
    sexo_lista = (
            ('M','Masculino'),
            ('F','Feminino'),
            ('N','Não desejo informar')
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sexo = models.CharField(max_length=1, choices=sexo_lista, blank=True, null=True)
    data_nascimento = models.DateField("Data de Nascimento", blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     UserProfile.objects.get_or_create(user=instance)

def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()