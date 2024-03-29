from hashlib import sha256
from django.http import HttpResponse
from django.shortcuts import redirect, render

#from home.views import verificaLogado
from users.views import db

categoriesDB = db['categories']

def categories(request):
    user = verificaLogado(request)

    if user['logado'] == True:
        ct = pegaCategorias(user['resposta']['id'])
        status = request.GET.get('status')
        return render(request, 'categories.html', {
            'user': user['resposta'],
            'categories': ct['itens'],
            'status': status
            }
        )
    else:
        return user['resposta']

def pegaCategorias(id_user):
    retorno = categoriesDB.find_one({'id_user': id_user})
    return retorno

def cadastraCat(request):
    status = request.GET.get('status')
    return render(request, 'cadastrar.html', {'status': status})

def validaCadCategories(request):
    a = request.session['user']
    name = request.POST['name']
    description = request.POST['description'],
    colorDesc = request.POST['colorDesc']
    cadCategorieBD(name, description, colorDesc, a['id'])
    return redirect('/categories/cadastraCat/?status=0')

def cadCategorieBD(name, description, color, id_user):
    categorias = pegaCategorias(id_user)
    cate = {
        'id': categorias['control']['last_id'] + 1,
        'name': name,
        'description': description[0],
        'color': color
    }
    categorias['control']['counter'] = categorias['control']['counter'] + 1
    categorias['control']['last_id'] = categorias['control']['last_id'] + 1
    categorias['itens'].append(cate)
    
    categoriesDB.update_one({'id_user': id_user},  {"$set": categorias })


def verificaLogado(request):
    """ 
        Retorna um dicionario, onde:
            'logado' é o estado se o usuário está ou não logado (True, False)
            'resposta'  pode ser o comando de redirecionar para a página de login (False);
                        pode ser o usuário para facilitar logo.
    """

    if ('user' in request.session):
        # Usuário está logado. 
        if request.session['user'] == None:
            return {'logado': False, 'resposta': redirect('/user/login/?status=1')}

    else:
        return {'logado': False, 'resposta': redirect('/user/login/?status=1')}
    
    return {'logado': True, 'resposta': request.session['user']}



# #ffff87
