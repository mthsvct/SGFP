from django.shortcuts import redirect, render
from django.http import HttpResponse
from hashlib import sha256


def home(request):
    aux = verificaLogado(request)

    if aux['logado'] == True:
        return render(request, 'home.html', {'user': aux['resposta']})
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
