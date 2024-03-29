from django.shortcuts import redirect, render
from django.http import HttpResponse
from hashlib import sha256

from users.views import db

def home(request):
    aux = verificaLogado(request)

    if aux['logado'] == True:
        id_user = request.session['user']['id']
        pg = db['pagamento'].find_one({'id_user': id_user})
        return render(request, 'home.html', {
            'user': aux['resposta'],
            'qnt_pagos': {
                'cartoes': len(pg['cartoes']['pagos']),
                'boletos': len(pg['boletos']['pagos']),
                'pix': len(pg['pix']['pagos']),
                'especie': len(pg['especie']['pagos']),
            }
            }
        )
    else:
        return aux['resposta']

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

def configuracoes(request):
    return render(request, 'configuracoes.html')

def sobre(request):
    return render(request, 'sobre.html')

def contato(request):
    return render(request, 'contato.html')