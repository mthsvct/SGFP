from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    #path('cadastro/', cadastro, name='cadastro')
    path('', despesas, name='despesas'),
    path('cadastrarDes/', cadastrarDes, name='cadastrarDes'),
    path('deleteDes/', deleteDes, name='deleteDes'),
    path('editarDes/', editarDes, name='editarDes'),
]