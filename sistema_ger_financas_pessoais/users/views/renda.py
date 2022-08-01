from hashlib import sha256
from django.http import HttpResponse
from django.shortcuts import redirect, render

from home.views import verificaLogado
from .cadastro import db, users


def renda(request):
    user = verificaLogado(request)
    if user['logado'] == True:
        status = request.GET.get('status')
        return render(request, 'renda.html', {
            'status': status,
            'user': user['resposta']
            }
        )
    else:
        return user['resposta']


def validaRenda(request):
    valor = float(request.POST['valor'])
    cadastrarRenda(valor, request.session['user']['id'])
    return redirect('/user/renda/?status=1')


def cadastrarRenda(valor, idU):
    users.update_one({'id': idU}, {"$set":{'renda': valor}})
