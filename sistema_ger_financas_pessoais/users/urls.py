from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('validaCadastro/', validaCadastro, name='validaCadastro'),
    path('login/', login, name='login'),
    path('validaLogin/', validaLogin, name='validaLogin'),
]