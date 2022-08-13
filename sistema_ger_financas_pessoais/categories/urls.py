from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', categories, name='categories'),
    path('cadastraCat/', cadastraCat, name='cadastraCat'),
    path('validaCadCategories/', validaCadCategories, name='validaCadCategories'),
    path('deleteCat/', deleteCat, name='deleteCat'),
    path('validaDeleteCat/', validaDeleteCat, name='validaDeleteCat'),
    path('editaCat/', editaCat, name='editaCat'),
    path('edit/<int:idCat>/', edit, name='edit'),
    path('validaEditCat/<int:idCat>/', validaEditCat, name='validaEditCat')
]