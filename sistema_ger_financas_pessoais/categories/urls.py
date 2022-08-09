from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', categories, name='categories'),
    path('cadastrar/', cadastrar, name='cadastrarCategories')
]