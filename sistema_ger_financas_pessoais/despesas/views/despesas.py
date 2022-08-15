from django.http import HttpResponse
from django.shortcuts import redirect, render

from users.views import db, atualizaControl

# Funções para apresentar as despesas.

despesasDB = db['despesas']

def despesas(request):
    id_user = request.session['user']['id']
    despesas = list(despesasDB.find({'id_user': id_user}))
    qnt = len(despesas)
    return render(request, 'despesas.html', {
        'id_user': id_user, 
        'despesas': despesas, 
        'qnt': qnt
        }
    )



