from django.http import HttpResponse
from django.shortcuts import redirect, render

from users.views import db, atualizaControl

# Funções para apresentar as despesas.

despesasDB = db['despesas']

def despesas(request):



    return render(request, 'despesas.html')
