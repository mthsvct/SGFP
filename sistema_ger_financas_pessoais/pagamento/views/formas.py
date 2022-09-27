from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient
from hashlib import sha256

from users.views import db, atualizaControl
from categories.views import categoriesDB, buscaCat
from despesas.views import despesasDB, buscaDespesa
from .pagamento import pgDB

def formas(request):
    id_user = request.session['user']['id']
    pg = pgDB.find_one({'id_user': id_user})
    cartoes = pg['cartoes']['personalizados']
    status = request.GET.get('status')
    return render(request, 'formas.html', 
        {
            'cartoes': cartoes,
            'qnt_cartoes': len(cartoes),
            'pagamento': pg,
            'qnt_pagos': {
                'cartoes': len(pg['cartoes']['pagos']),
                'boletos': len(pg['boletos']['pagos']),
                'pix': len(pg['pix']['pagos']),
                'especie': len(pg['especie']['pagos']),
            },
            'status': status
        }
    )