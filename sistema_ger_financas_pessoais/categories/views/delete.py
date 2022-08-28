from ctypes import cast
from hashlib import sha256
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .categories import categoriesDB

def deleteCat(request):
    user = request.session['user']
    cats = list(categoriesDB.find({'id_user': user['id']}))
    qnt = len(cats)
    status = request.GET.get('status')
    return render(request, 'deleteCat.html', {
        'user': user['id'], 
        'categorias': cats, 
        'status': status,
        'qnt': qnt
        }
    )

def  deleteDB(deletes, collection, id_user):
    c = collection.find_one({'id_user': id_user})
    for i in deletes:
        c['itens'].pop( i['index'] )
    c['control']['counter'] = len( c['itens'] )
    collection.update_one(
        {'id_user': id_user},
        {"$set": c}
    ) # Atualiza

def pegaSelecoesDelete(post, id_user, collection):
    deletes = []
    d = collection.find_one({'id_user': id_user})
    
    for j, i in enumerate(d['itens']):
        if (f'select{i["id"]}') in post:
            deletes.append(
               {'id': i['id'], 'index': j}
            )

    return deletes

def validaDeleteCat(request):
    id_user = request.session['user']['id']
    deletes = pegaSelecoesDelete(request.POST, id_user, categoriesDB)
    if len(deletes) > 0:
        deleteDB(deletes, categoriesDB, id_user)
    else:
        return redirect('/categories/deleteCat/?status=1')
    return redirect('/categories/deleteCat/?status=0')
