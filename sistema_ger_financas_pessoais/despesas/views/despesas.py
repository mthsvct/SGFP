from django.http import HttpResponse
from django.shortcuts import redirect, render

from users.views import db, atualizaControl

# Funções para apresentar as despesas.

despesasDB = db['despesas']

def despesas(request):
    id_user = request.session['user']['id']
    despesas = despesasDB.find_one({'id_user': id_user})
    """ print(despesas) """
    qnt = len(despesas['itens'])
    return render(request, 'despesas.html', {
        'id_user': id_user,
        'despesas': list(despesas['itens']),
        'qnt': qnt
        }
    )



