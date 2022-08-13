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

def deleteDB(deletes):
    for i in deletes:
        categoriesDB.delete_one({'id': i})
        c = categoriesDB.find_one({"id": 0})
        counter = c['counter'] - 1
        categoriesDB.update_one({'id': 0}, {"$set":{'counter': counter}})

def pegaSelecoesDelete(post, id_user):
    deletes = []
    for i in list(categoriesDB.find({'id_user': id_user})):
        print(f'select{i["id"]}')
        if (f'select{i["id"]}') in post:
            deletes.append(i['id'])
    return deletes

def validaDeleteCat(request):
    #return HttpResponse('select9' in request.POST)
    deletes = pegaSelecoesDelete(request.POST, request.session['user']['id'])
    
    print(deletes)

    if len(deletes) > 0:
        deleteDB(deletes)
    else:
        return redirect('/categories/deleteCat/?status=1')

    return redirect('/categories/deleteCat/?status=0')
