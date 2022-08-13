from hashlib import sha256
from django.http import HttpResponse
from django.shortcuts import redirect, render

from home.views import verificaLogado
from users.views import db, atualizaControl

categoriesDB = db['categories']

def categories(request):
    user = verificaLogado(request)

    if user['logado'] == True:
        ct = pegaCategorias(user['resposta']['id'])
        status = request.GET.get('status')
        return render(request, 'categories.html', {
            'user': user['resposta'],
            'categories': ct,
            'status': status
            }
        )
    else:
        return user['resposta']

def pegaCategorias(id_user):

    padroes = list(categoriesDB.find({'id_user': -1}))
    personalizadas = list(categoriesDB.find({'id_user': id_user}))

    todos = []

    for i in padroes:
        todos.append(i)

    for j in personalizadas:
        todos.append(j)

    return todos

def cadastraCat(request):
    status = request.GET.get('status')
    return render(request, 'cadastrar.html', {'status': status})

def validaCadCategories(request):
    a = request.session['user']
    name = request.POST['name']
    description = request.POST['description'],
    colorDesc = request.POST['colorDesc']
    cadCategorieBD(name, description, colorDesc, a['id'])
    return redirect('/categories/cadastrar/?status=0')

def cadCategorieBD(name, description, color, id_user):
    c = categoriesDB.find_one({"id": 0})
    cate = {
        'id': c['last_id'] + 1,
        'name': name,
        'description': description[0],
        'color': color,
        'type': 1,
        'id_user': id_user
    }
    categoriesDB.insert_one(cate)
    atualizaControl(categoriesDB)

# #ffff87
