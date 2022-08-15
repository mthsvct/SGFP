from django.http import HttpResponse
from django.shortcuts import redirect, render

from .despesas import despesasDB
from categories.views import categoriesDB, pegaCategorias

def editarDes(request):
    id_user = request.session['user']['id']
    despesas = list(despesasDB.find({'id_user': id_user}))
    qnt = len(despesas)
    return render(request, 'editarDes.html', {
        'id_user': id_user, 
        'despesas': despesas, 
        'qnt': qnt
        }
    )

def editDes(request, idDes):
    id_user = request.session['user']['id']
    des = despesasDB.find_one({'id': idDes})
    cats = pegaCategorias(id_user)
    status = request.GET.get('status')
    return render(request, 'editD.html', {
        'id_user': id_user,
        'despesa': des,
        'categorias': cats,
        'status': status
        }
    )

def validaEditDes(request, idDes):
    
    name = request.POST['name']
    des = request.POST['description']
    valor = request.POST['valor']
    vencimento = request.POST['vencimento']
    cat = int(request.POST['categoria'])
    id_user = request.session['user']['id']

    despesasDB.update_one(
        {'id': idDes}, 
        {"$set": {
            'name': name, 
            'description': des, 
            'valor': valor,
            'vencimento': vencimento,
            'categoria': cat,
            'id_user': id_user
            }
        }
    )

    return redirect(f'/despesas/editDes/{idDes}/?status=0')
