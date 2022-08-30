from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('<int:idDes>/', pagamento, name='pagamento'),
    path('', pagamentos, name='pagamentos'),
    path('validaPagamento/<int:idDes>/', validaPagamento, name='validaPagamento')
]