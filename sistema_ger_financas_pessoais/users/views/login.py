from hashlib import sha256
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .cadastro import db, users

# Create your views here.
def login(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})


def validaLogin(request):
    # Verificações:
        #[  ] 1 - Verificar se este email está cadastrado.
        #[  ] 2 - Verificar se a senha está correta.

    email = request.POST['email']
    password = sha256(request.POST['password'].encode()).hexdigest()

    user = buscaUser(email)

    if len(user) == 0:
        #return HttpResponse(f'Email não encontrado!')
        return redirect('/user/login/?status=3')
        
    elif verificaPass(user[0], password) == False:
        #return HttpResponse(f'Senha incorreta!')
        return redirect('/user/login/?status=4')


    request.session['user'] = {'id': user[0]['id'], 'name': user[0]['name']}

    return redirect('home')


def buscaUser(email):
    user = users.find({'email': email})
    return list(user)


def verificaPass(user, password):
    if user['password'] == password:
        return True
    else:
        return False


def sair(request):
    request.session['user'] = None
    return redirect('/user/login/')

