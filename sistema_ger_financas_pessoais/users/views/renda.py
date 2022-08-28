from datetime import date
from hashlib import sha256
from django.http import HttpResponse
from django.shortcuts import redirect, render

from home.views import verificaLogado
from .cadastro import db, users
from despesas.views import montaData


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
    saldo = float(request.POST['saldo'])
    valor = float(request.POST['valor'])
    dia = montaData(request.POST['dia'])

    """ separado = request.POST['dia'].split('-')
    dia = date(
        int(separado[0]),
        int(separado[1]),
        int(separado[2]),
    ) # Montei a data a partir da string vinda do formulário. """

    cadastrarRenda(saldo, valor, dia, request.session['user']['id'])
    return redirect('/user/renda/?status=1')

def cadastrarRenda(saldo, valor, dia, idU):
    users.update_one({'id': idU}, {
        "$set":{
            'renda': {
                'saldo': saldo,
                'renda_mensal': valor, 
                'data': dia.strftime("%Y-%m-%d")
                }
            }
        }
    )
