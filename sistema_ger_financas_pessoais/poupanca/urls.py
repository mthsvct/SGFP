from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    #path('cadastro/', cadastro, name='cadastro')
    path('', poupanca, name='poupanca'),
    path('configurar/', configurar, name='configurar'),
    path('validaConfigPoup/', validaConfigPoup, name='validaConfigPoup')
]