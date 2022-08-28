from ctypes import cast
from hashlib import sha256
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .categories import categoriesDB, pegaCategorias

def editaCat(request):
    id_user = request.session['user']['id']
    categorias = categoriesDB.find_one({'id_user': id_user})
    return render(request, 'selCat.html', {'categorias': categorias})

def buscaCat(idCat, categoria):
    retorno = None
    index = -1
    for j, i in enumerate(categoria['itens']):
        if i['id'] == idCat:
            retorno = i
            index = j
    return retorno, index

def edit(request, idCat):
    status = request.GET.get('status')
    id_user = request.session['user']['id']
    categoria = categoriesDB.find_one({'id_user': id_user})
    cat, _ = buscaCat(idCat, categoria)
    return render(request, 'edit.html', {'categoria': cat, 'idCat': idCat, 'status': status})

def validaEditCat(request, idCat):
    name = request.POST['name']
    des = request.POST['description']
    color = request.POST['colorDesc']
    id_user = request.session['user']['id']

    categoria = categoriesDB.find_one({'id_user': id_user})
    _, indice = buscaCat(idCat, categoria)

    print(indice)
    print(categoria)

    print('*' * 100)

    categoria['itens'][indice] = {
        'id': categoria['itens'][indice]['id'],
        'name': name,
        'description': des,
        'color': color
    }

    print(categoria)

    categoriesDB.update_one(
        {'id_user': id_user}, 
        {"$set": categoria}
    )

    return redirect(f'/categories/edit/{idCat}/?status=0')
