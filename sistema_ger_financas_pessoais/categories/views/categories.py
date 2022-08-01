from hashlib import sha256
from django.http import HttpResponse
from django.shortcuts import redirect, render

from home.views import verificaLogado
from users.views import db

categoriesDB = db['categories']

def categories(request):
    user = verificaLogado(request)

    

    if user['logado'] == True:
        ct = pegaCategorias(user['resposta']['id'])
        return render(request, 'categories.html', {
            'user': user['resposta'],
            'categories': ct
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

# #ffff87
