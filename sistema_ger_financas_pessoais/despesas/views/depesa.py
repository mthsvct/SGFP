from django.http import HttpResponse
from django.shortcuts import redirect, render

from users.views import db, atualizaControl
from categories.views import categoriesDB, buscaCat
from .despesas import despesasDB
from .editar import buscaDespesa

def despesa(request, idDes):
    id_user = request.session['user']['id']
    d = despesasDB.find_one({'id_user': id_user})
    des, indiceD = buscaDespesa(d['itens'], idDes)
    c = categoriesDB.find_one({'id_user': id_user})
    cat, indiceC = buscaCat(des['categoria'], c)
    return render(request, 'despesa.html', {'despesa': des, 'categoria': cat})