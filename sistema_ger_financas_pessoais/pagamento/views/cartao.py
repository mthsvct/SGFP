from datetime import date
from re import I
from django.shortcuts import redirect, render
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient
from hashlib import sha256

from users.views import db, atualizaControl
from categories.views import categoriesDB, buscaCat
from despesas.views import despesasDB, buscaDespesa


pgDB = db['pagamento']

class Cartao():

    def __init__(self, banco='', limite=float(0), vencimento='', id_user=-1):
        self.banco = banco
        self.id = -1
        self.limite = limite
        self.vencimento = vencimento
        self.utilizado = float(0)
        self.id_user = id_user
        self.pagos = []
        self.indice = -1
    
    def sequencia(self):
        self.monta_id()
        self.salva_cartao()
    
    def monta_id(self):
        p = pgDB.find_one({'id_user': self.id_user})
        self.id = p['cartoes']['control']['last_id'] + 1
        p['cartoes']['control']['last_id'] = self.id
        pgDB.update_one({'id_user': self.id_user}, {'$set': p})

    def monta_objeto(self):
        return {
            'id': self.id,
            'banco': self.banco,
            'limite': self.limite,
            'utilizado': self.utilizado,
            'vencimento': self.vencimento,
            'pagos': self.pagos
        }

    def salva_cartao(self):
        p = pgDB.find_one({'id_user': self.id_user})
        p['cartoes']['personalizados'].append(self.monta_objeto())
        pgDB.update_one({'id_user': self.id_user}, {'$set': p})

    def monta_cartao(self, id_cartao):
        p = pgDB.find_one({'id_user': self.id_user})
        c, self.indice = busca_cartao(id_cartao, p['cartoes']['personalizados'])

        if c != None:
            self.banco = c['banco']
            self.id = c['id']
            self.limite = c['limite']
            self.vencimento = c['vencimento']
            self.utilizado = c['utilizado']
            self.id_user = p['id_user']
            self.pagos = c['pagos']

    def add_pagamento(self, pagamento):
        p = pgDB.find_one({'id_user': self.id_user})
        p['cartoes']['personalizados'][self.indice]['pagos'].append(pagamento['id'])
        pgDB.update_one({'id_user': self.id_user}, {'$set': p})
        self.monta_cartao(self.id)

def busca_cartao(id_cartao, cartoes):
    retorno = None
    indice = -1
    for index, i in enumerate(cartoes):
        if id_cartao == i['id']:
            retorno = i
            indice = index
    return retorno, indice

def cadastrar_cartao(request):
    status = request.GET.get('status')
    return render(request, 'cadastrar_cartao.html', {'status': status})
    
def validaCadCartao(request):
    id_user = request.session['user']['id']
    banco = request.POST['banco']
    limite = request.POST['limite']
    vencimento = request.POST['vencimento']
    Cartao(banco, float(limite), vencimento, id_user).sequencia()
    return redirect(f'/pagamento/cadastrar_cartao/?status=0')

def buscaPagamento(pagamento, idPg):
    for i in pagamento['itens']:
        if idPg == i['id']:
            return i

    return None

def verTipo(tipo):
    if tipo == 1:
        return 'boletos'
    elif tipo == 2:
        return 'pix'
    elif tipo == 3:
        return 'especie'
    else:
        return 'cartoes'

def pegaPagamentos(cartao, id_user):
    retorno = []
    d = despesasDB.find_one({'id_user': id_user})
    p = pgDB.find_one({'id_user': id_user})

    for i in cartao.pagos:
        pg = buscaPagamento(p, i)
        print('\n\n', pg, '\n\n')
        despesa, _ = buscaDespesa(d['itens'], pg.get('id_des'))

        retorno.append(
            {
                'pagamento': pg,
                'despesa': despesa,
                'tipo': verTipo(pg['tipo']).upper()
            }
        )

    return retorno

def cartao(request, idCartao):
    id_user = request.session['user']['id']
    c = Cartao(id_user=id_user)
    c.monta_cartao(idCartao)
    o = c.monta_objeto()
    qnt = len(o['pagos'])
    pagamentos = pegaPagamentos(c, id_user)
    return render(request, 'cartao.html', {
        'cartao': o,
        'qnt': qnt,
        'pagamentos': pagamentos
    })

def registraPagamentoNoCartao(pagamento, cartao):
    c = Cartao(id_user=pagamento['id_user'])
    c.monta_cartao(cartao)
    c.add_pagamento(pagamento)



