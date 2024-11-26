from django.contrib import admin
from .models import Pergunta, Resposta, UserProfile

admin.site.register(Pergunta)
admin.site.register(Resposta)
admin.site.register(UserProfile)

# Register your models here.
