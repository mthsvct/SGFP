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
    path('cartao/<int:idCartao>/', cartao, name='cartao')
]