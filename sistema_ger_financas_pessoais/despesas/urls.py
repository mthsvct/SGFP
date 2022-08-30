from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    #path('cadastro/', cadastro, name='cadastro')
    path('', despesas, name='despesas'),
    path('cadastrarDes/', cadastrarDes, name='cadastrarDes'),
    path('validaCadDes/', validaCadDes, name='validaCadDes'),
    path('deleteDes/', deleteDes, name='deleteDes'),
    path('validaDeleteDes/', validaDeleteDes, name='validaDeleteDes'),
    path('editarDes/', editarDes, name='editarDes'),
    path('editDes/<int:idDes>/', editDes, name='editDes'),
    path('validaEditDes/<int:idDes>/', validaEditDes, name='validaEditDes'),
    path('<int:idDes>/', despesa, name='despesa'),
]