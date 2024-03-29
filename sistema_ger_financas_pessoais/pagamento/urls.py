from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('<int:idDes>/', pagamento, name='pagamento'),
    path('', pagamentos, name='pagamentos'),
    path('validaPagamento/<int:idDes>/', validaPagamento, name='validaPagamento'),
    path('formas/', formas, name='formas'),
    path('cadastrar_cartao/', cadastrar_cartao, name='cadastrar_cartao'),
    path('validaCadCartao/', validaCadCartao, name='validaCadCartao'),
    path('cartao/<int:idCartao>/', cartao, name='cartao'),
    path('edita_cartao/<int:idCartao>/', edita_cartao, name='edita_cartao'),
    path('valida_edita_cartao/<int:idCartao>/', valida_edita_cartao, name='valida_edita_cartao'),
    path('exclui_cartao/<int:idCartao>/', exclui_cartao, name='exclui_cartao'),
]