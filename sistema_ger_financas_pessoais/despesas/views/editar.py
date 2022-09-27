from django.http import HttpResponse
from django.shortcuts import redirect, render

from .despesas import despesasDB
from categories.views import categoriesDB, pegaCategorias
from .cadastro import pegaStatus

def editarDes(request):
    id_user = request.session['user']['id']
    despesas = despesasDB.find_one({'id_user': id_user})
    qnt = len(despesas['itens'])
    return render(request, 'editarDes.html', {
        'id_user': id_user, 
        'despesas': despesas['itens'], 
        'qnt': qnt
        }
    )

def buscaDespesa(despesas, idDes):
    retorno = None
    indice = -1
    for index, i in enumerate(despesas):
        if i['id'] == idDes:
            retorno = i
            indice = index
    return retorno, indice

def editDes(request, idDes):
    id_user = request.session['user']['id']
    des = despesasDB.find_one({'id_user': id_user})
    despesa, _ = buscaDespesa(des['itens'], idDes)
    valores = {
        'completo': str(despesa['valor']['completo']),
        'pago': str(despesa['valor']['pago'])
    }
    cats = pegaCategorias(id_user)
    status = request.GET.get('status')
    return render(request, 'editD.html', {
        'id_user': id_user,
        'categorias': cats['itens'],
        'despesa': despesa,
        'valores': valores,
        'status': status
        }
    )

def validaEditDes(request, idDes):
    id_user = request.session['user']['id']
    d = despesasDB.find_one({'id_user': id_user})
    _, indice = buscaDespesa(d['itens'], idDes)

    name = request.POST['name']
    des = request.POST['description']
    valor = float(request.POST['valor'])
    pago = float(request.POST['pago'])
    restante = float(request.POST['valor']) - pago
    vencimento = request.POST['vencimento']
    cat = int(request.POST['categoria'])
    id_user = request.session['user']['id']

    d['itens'][indice] = {
        'id': d['itens'][indice]['id'],
        'name': name,
        'description': des,
        'valor': {
            'completo': float(valor),
            'restante': float(restante),
            'pago': float(pago)
        },
        'vencimento': vencimento,
        'categoria': cat,
        'id_user': id_user,
        'status': pegaStatus(vencimento)
    }

    despesasDB.update_one(
        {'id_user': id_user}, 
        {"$set": d}
    ) # Atualiza
    
    return redirect(f'/despesas/editDes/{idDes}/?status=0')

def buscaPagamento_despesa(despesa, indice, idP):
    for index, i in enumerate(despesa['itens'][indice]['pagamento']):
        if i == idP:
            return i, index
    return None, -1
