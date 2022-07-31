from django.shortcuts import redirect, render
from django.http import HttpResponse
from hashlib import sha256


def home(request):
    if 'user' in request.session:
        # Usuário está logado.
        user = request.session['user']
    else:
        return redirect('/user/login/?status=1')

    return render(request, 'home.html', {'user': user})