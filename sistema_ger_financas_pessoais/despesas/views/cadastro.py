from django.http import HttpResponse
from django.shortcuts import redirect, render
from datetime import date

from categories.views import pegaCategorias
from users.views import atualizaControl
from .despesas import despesasDB

def cadastrarDes(request):
    user = request.session.get('user')
    categorias = pegaCategorias(user['id'])
    hoje = date.today().strftime('%Y-%m-%d')
    status = request.GET.get('status')
    return render(request, 'cadastrarDes.html', {'categorias': categorias, 'hoje': hoje, 'status': status})

def validaCadDes(request):

    name = request.POST['name']
    des = request.POST['description']
    valor = request.POST['valor']
    vencimento = request.POST['vencimento']
    cat = int(request.POST['categoria'])
    id_user = request.session['user']['id']

    salvar_des_BD(name, des, valor, vencimento, cat, id_user)
    
    return redirect('/despesas/cadastrarDes/?status=0')

def salvar_des_BD(name, des, valor, vencimento, cat, id_user):
    # Salva uma nova despesa no banco de dados.
    c = despesasDB.find_one({"id": 0})
    d = {
        'id': c['last_id'] + 1,
        'name': name,
        'description': des,
        'valor': valor,
        'vencimento': vencimento,
        'categoria': cat,
        'id_user': id_user
    }

    despesasDB.insert_one(d)
    atualizaControl(despesasDB)
