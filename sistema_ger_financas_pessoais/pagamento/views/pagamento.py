from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient
from hashlib import sha256

from users.views import db, atualizaControl
from categories.views import categoriesDB, buscaCat
from despesas.views import despesasDB, buscaDespesa
from .cartao import registraPagamentoNoCartao
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

def verTipo(tipo):
    if tipo == 1:
        return 'boletos'
    elif tipo == 2:
        return 'pix'
    elif tipo == 3:
        return 'especie'
    else:
        return 'cartoes'

def adicionaDespesaNaForma(tipo, id_pg, id_user, cartao):
    pg = pgDB.find_one({'id_user': id_user})
    t = verTipo(tipo)
    id_cartao = cartao
    pg[t]['pagos'].append(
        {
            'id_pg': id_pg,
            'id_cartao': id_cartao
        }
    )
    return pg

def efetuarPagamento(id_user, pagamento, ind_des):
    despesa = despesasDB.find_one({'id_user': id_user})
    restante = despesa['itens'][ind_des]['valor']['restante'] - pagamento['valor']
    despesa['itens'][ind_des]['valor']['restante'] = round(restante, 2)
    despesa['itens'][ind_des]['valor']['pago'] += pagamento['valor']

    if despesa['itens'][ind_des]['valor']['restante'] <= 0:
        despesa['itens'][ind_des]['status'] = 1

    #despesa['itens'][ind_des]['pagamento'].append(pagamento['id'])
    despesasDB.update_one({'id_user': id_user}, {'$set': despesa})

def criaPagamentoBasico(id_user, id_des, valor, data, tipo, cartao, ind_des):
    pagamento = pgDB.find_one({'id_user': id_user})
    
    p = {
        'id': pagamento['control']['last_id'] + 1,
        'id_user': id_user,
        'id_des': id_des,
        'valor': valor,
        'data': data,
        'tipo': tipo
    }

    pagamento['control']['last_id'] += 1
    pgDB.update_one({'id_user': id_user}, {'$set': pagamento})

    pagamento = pgDB.find_one({'id_user': id_user})
    efetuarPagamento(id_user, p, ind_des) # diminui os valores da despesa de acordo com o pagamento efetuado
    pagamento = adicionaDespesaNaForma(tipo, p['id'], id_user, cartao)
    pagamento['itens'].append(p) # é inserido o registro de pagamento no array vindo do banco de dados
    pagamento['control']['counter'] = len(pagamento['itens'])
    pgDB.update_one({'id_user': id_user}, {'$set': pagamento}) # o banco de dados é atualizado.
    
    if cartao != None:
        registraPagamentoNoCartao(p, cartao)

def validaPagamento(request,  idDes):
    id_user = request.session['user']['id']
    tipo = int(request.POST['tipo'])
    valor = float(request.POST['valor'])

    if 'cartao' in request.POST:
        cartao = int(request.POST['cartao'])
    else:
        cartao = -1

    data = request.POST['data']

    d = despesasDB.find_one({'id_user': id_user})
    des, indiceD = buscaDespesa(d['itens'], idDes)

    if tipo < 4:
        criaPagamentoBasico(id_user, des['id'], valor, data, tipo, None, indiceD)
    else:
        criaPagamentoBasico(id_user, des['id'], valor, data, tipo, cartao, indiceD)

    return redirect(f'/pagamento/{idDes}/?status=0')

