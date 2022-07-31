from django.shortcuts import redirect, render
from django.http import HttpResponse
from hashlib import sha256
from .cadastro import db, users, buscaRepetido


def esqueceuSenha(request):
    status = request.GET.get('status')
    return render(request, 'esqueceuSenha.html', {'status': status})


def validaEsqueceuSenha(request):

    email = request.POST['email']
    new_p = request.POST['password']
    new_confirm = request.POST['confirm_password']

    if new_p != new_confirm:
        return redirect('/user/esqueceuSenha/?status=1')
    elif buscaRepetido(email) == 0:
        return redirect('/user/esqueceuSenha/?status=2')

    u = users.find_one({'email': email})
    new_p_crypt = sha256(new_p.encode()).hexdigest()

    users.update_one({'id': u['id']}, {"$set":{'password': new_p_crypt}})

    return redirect('/user/login/')
