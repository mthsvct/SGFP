from datetime import date
from math import ceil
from django.http import HttpResponse
from django.shortcuts import redirect, render
from dateutil.relativedelta import relativedelta

from users.views import db

poupDB = db['poupanca']

# Funções para apresentar as despesas.

def poupanca(request):
    id_user = request.session['user']['id']
    p = poupDB.find_one({'id_user': id_user})
    status = request.GET.get('status')
    return render(request, 'poupanca.html', {
        'id_user': id_user,
        'poupanca': p,
        'status': status
        }
    )

def configurar(request):
    id_user = request.session['user']['id']
    p = poupDB.find_one({'id_user': id_user})
    valores = {
        'guardado': str(p['guardado']),
        'mensal': str(p['mensal']),
        'planejado': str(p['planejado'])
    }
    return render(request, 'configurarPoup.html', {
        'id_user': id_user,
        'poupanca': p,
        'valores': valores
        }
    )

def calculaTempoPoup(planejado, mensal, guardado):
    # Incrementar a funcionalidade
    meses = ((planejado - guardado) / mensal)
    m = ceil(meses)
    data =  date.today() + relativedelta(months=+m)
    return {'meses': m, 'data': data.strftime('%Y-%m-%d')}

def editaPoup(planejado, mensal, guardado, data, id_user):
    p = poupDB.find_one({'id_user': id_user})

    p['planejado'] = planejado
    p['mensal'] = mensal
    p['guardado'] = guardado
    p['data'] = data

    poupDB.update_one(
        {'id_user': id_user},
        {"$set": p}
    )

def validaConfigPoup(request):
    # Editar no banco de dados.
    # Calcular tempo.
    id_user = request.session['user']['id']

    planejado = float(request.POST['planejado'])
    mensal = float(request.POST['mensal'])
    guardado = float(request.POST['guardado'])

    if mensal > 0:
        data = calculaTempoPoup(planejado, mensal, guardado)
    else:
        data = {'meses': -1, 'data': None}

    editaPoup(planejado, mensal, guardado, data, id_user)
    return redirect('/poupanca/?status=0')
