from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "polls"

urlpatterns = [
    path("registro/", views.registro, name="Registro"),
    path("login/", views.login_view, name="Login"),
    path("logout/", views.logout_view, name="Logout"),
    path("teste/", views.teste, name="Teste"),
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="Detalhe"),
    path("<int:pergunta_id>/results/", views.ResultsView, name="Resultados"),
    path("<int:pergunta_id>/vote/", views.vote, name="Votos"),
    path("altera/", views.altera_cadastro, name="AlteraCadastro"),
    path("altera_senha/", auth_views.PasswordChangeView.as_view(template_name='polls/altera_senha.html'), name="AlteraSenha"),
]