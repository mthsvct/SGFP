from ctypes import cast
from hashlib import sha256
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .categories import categoriesDB, pegaCategorias

def editaCat(request):
    categorias = list(categoriesDB.find({'id_user': request.session['user']['id']}))
    return render(request, 'selCat.html', {'categorias': categorias})

def edit(request, idCat):
    status = request.GET.get('status')
    cat = categoriesDB.find_one({'id': idCat})
    return render(request, 'edit.html', {'cat': cat, 'idCat': idCat, 'status': status})

def validaEditCat(request, idCat):
    name = request.POST['name']
    des = request.POST['description']
    color = request.POST['colorDesc']
    categoriesDB.update_one({'id': idCat}, {"$set":{'name': name, 'description': des, 'color': color}})
    return redirect(f'/categories/edit/{idCat}/?status=0')
