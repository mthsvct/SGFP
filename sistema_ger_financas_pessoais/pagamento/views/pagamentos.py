from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient
from hashlib import sha256

from users.views import db, atualizaControl
from categories.views import categoriesDB, buscaCat
from despesas.views import despesasDB, buscaDespesa

from .pagamento import pgDB, verTipo

def pagamentos(request):
    # Aqui será a tela que apresentará a funcionalidade de editar cartões
    id_user = request.session['user']['id']
    p = pgDB.find_one({'id_user': id_user})
    d = despesasDB.find_one({'id_user': id_user})
    pgs = []

    for i in p['itens']:
        des, ind_des = buscaDespesa(d['itens'], i['id_des'])
        pgs.append(
            {
                'despesa': des,
                'pagamento': i,
                'tipo': verTipo(i['tipo']).upper()
            }
        )

    return  render(request, 'pagamentos.html', {'pagamentos': pgs, 'qnt': len(pgs)})


