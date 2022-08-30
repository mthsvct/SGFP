from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('configuracoes/', configuracoes, name='configuracoes'),
    path('sobre/', sobre, name='sobre'),
    path('contato/', contato, name='contato')
]
