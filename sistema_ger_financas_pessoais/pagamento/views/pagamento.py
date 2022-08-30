from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient
from hashlib import sha256

from users.views import db, atualizaControl
from categories.views import categoriesDB, buscaCat
from despesas.views import despesasDB, buscaDespesa

# -----------------------------
pgDB = db['pagamento']


def pagamento(request, idDes):
    id_user = request.session['user']['id']
    d = despesasDB.find_one({'id_user': id_user})
    des, indiceD = buscaDespesa(d['itens'], idDes)
    c = categoriesDB.find_one({'id_user': id_user})
    cat, indiceC = buscaCat(des['categoria'], c)
    pg = pgDB.find_one({'id_user': id_user})
    status = request.GET.get('status')
    return render(request, 'pagamento.html', 
        {
            'despesa': des, 
            'categoria': cat, 
            'formas': pg, 
            'idDes': des['id'],
            'valor_max': str(des['valor']['restante']),
            'status': status
        }
    )

def criaPagamentoBasico(tipo, valor, id_user, despesa, data):
    p = {
        'pago': valor,
        'data': data,
        'tipo': tipo
    }

    despesa['valor']['restante'] = despesa['valor']['restante'] - valor
    despesa['valor']['pago'] = despesa['valor']['pago'] + valor
    despesa['pagamento'].append(p)
    return despesa

def verTipo(tipo):
    if tipo == 1:
        return 'boletos'
    elif tipo == 2:
        return 'pix'
    elif tipo == 3:
        return 'especie'

def adicionaDespesaNaForma(tipo, idDes, id_user):
    pg = pgDB.find_one({'id_user': id_user})
    t = verTipo(tipo)
    pg[t]['pagos'].append(idDes)
    pgDB.update_one({'id_user': id_user}, {'$set': pg})

def validaPagamento(request,  idDes):
    id_user = request.session['user']['id']
    tipo = int(request.POST['tipo'])
    valor = float(request.POST['valor'])
    data = request.POST['data']

    d = despesasDB.find_one({'id_user': id_user})
    des, indiceD = buscaDespesa(d['itens'], idDes)

    if tipo < 4:
        adicionaDespesaNaForma(tipo, idDes, id_user)
        d['itens'][indiceD] = criaPagamentoBasico(tipo, valor, id_user, des, data)

    despesasDB.update_one({'id_user': id_user}, {'$set': d})

    return redirect(f'/pagamento/{idDes}/?status=0')

def pagamentos(request):
    # Aqui será a tela que apresentará a funcionalidade de editar cartões
    return HttpResponse('Hello World!')

