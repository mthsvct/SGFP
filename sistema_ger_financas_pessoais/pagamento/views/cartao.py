from datetime import date
from re import I
from django.shortcuts import redirect, render
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient
from hashlib import sha256

from users.views import db, atualizaControl
from categories.views import categoriesDB, buscaCat
from despesas.views import despesasDB, buscaDespesa, pegaStatus, buscaPagamento_despesa


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
        
        return self

    def add_pagamento(self, pagamento):
        p = pgDB.find_one({'id_user': self.id_user})
        p['cartoes']['personalizados'][self.indice]['pagos'].append(pagamento['id'])
        pgDB.update_one({'id_user': self.id_user}, {'$set': p})
        self.monta_cartao(self.id)
    
    def salvar(self):
        p = pgDB.find_one({'id_user': self.id_user})
        p['cartoes']['personalizados'][self.indice] = self.monta_objeto()
        pgDB.update_one({'id_user': self.id_user}, {'$set': p})

    def editar(self, banco, limite, vencimento):
        self.banco = banco
        self.limite = limite
        self.vencimento = vencimento
        self.salvar()

    def volta_despesa(self):
        p = pgDB.find_one({'id_user': self.id_user})
        d = despesasDB.find_one({'id_user': self.id_user})

        for i in self.pagos:
            # Remover da lista dos itens pagos por cartoes:
            # remove = []

            for index, j in enumerate(p['cartoes']['pagos']):
                if j['id_cartao'] == self.id:
                    p['cartoes']['pagos'].remove(j)
            
            # Remover da lista do itens dos pagamentos:
            for index2, j in enumerate(p['itens']):
                if j['id'] == i:

                    _, indiceD = buscaDespesa(d['itens'], j['id_des'])

                    d['itens'][indiceD]['valor']['pago'] = d['itens'][indiceD]['valor']['pago'] - j['valor']
                    d['itens'][indiceD]['valor']['restante'] = d['itens'][indiceD]['valor']['completo'] - d['itens'][indiceD]['valor']['pago']

                    p['itens'].remove(j)  
        
        pgDB.update_one({'id_user': self.id_user}, {'$set': p})
        despesasDB.update_one({'id_user': self.id_user}, {'$set': d})

    def excluir(self):

        if len(self.pagos) > 0:
            self.volta_despesa()
            # print('Ah, mas que pertubação!!!!!!!!!!!!')
        
        p = pgDB.find_one({'id_user': self.id_user})
        p['cartoes']['personalizados'].pop(self.indice)
        pgDB.update_one({'id_user': self.id_user}, {'$set': p})



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
    for index, i in enumerate(pagamento['itens']):
        if idPg == i['id']:
            return i, index

    return None, -1

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
        pg, _ = buscaPagamento(p, i)
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

def edita_cartao(request, idCartao):
    id_user = request.session['user']['id']
    c = Cartao(id_user = id_user)
    c.monta_cartao(idCartao)
    cartao = c.monta_objeto()
    status = request.GET.get('status')
    return render(request, 'edita_cartao.html', {
        'cartao': cartao,
        'limite': str(cartao['limite']),
        'status': status
        }
    )

def valida_edita_cartao(request, idCartao):
    id_user = request.session['user']['id']
    c = Cartao(id_user=id_user)
    c.monta_cartao(idCartao)

    c.editar(
        banco=request.POST['banco'],
        limite=float(request.POST['limite']),
        vencimento=request.POST['vencimento']
    )

    return redirect(f'/pagamento/edita_cartao/{idCartao}/?status=0')

def exclui_cartao(request, idCartao):
    id_user = request.session['user']['id']
    c = Cartao(id_user=id_user).monta_cartao(idCartao)
    c.excluir()
    return redirect('/pagamento/formas/?status=1')

def buscaPagamentoNoTipo(pagamentos, indice, idP, tipo):
    for index, i in enumerate(pagamentos[verTipo(tipo)]['pagos']):
        if i['id_pg'] == idP:
            return i, index
    return None, -1
