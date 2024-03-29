from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('validaCadastro/', validaCadastro, name='validaCadastro'),
    path('login/', login, name='login'),
    path('validaLogin/', validaLogin, name='validaLogin'),
    path('esqueceuSenha/', esqueceuSenha, name='esqueceuSenha'),
    path('validaEsqueceuSenha/', validaEsqueceuSenha, name='validaEsqueceuSenha'),
    path('sair/', sair, name='sair'),
    path('renda/', renda, name='renda'),
    path('validaRenda/', validaRenda, name='validaRenda'),
    path('excluirConta/', excluirConta, name='excluirConta')
]