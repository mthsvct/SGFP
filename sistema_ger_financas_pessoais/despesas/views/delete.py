from django.http import HttpResponse
from django.shortcuts import redirect, render

from .despesas import despesasDB
from categories.views import pegaSelecoesDelete, deleteDB

def deleteDes(request):
    id_user = request.session['user']['id']
    despesas = despesasDB.find_one({'id_user': id_user})
    status = request.GET.get('status')
    qnt = len(despesas['itens'])
    return render(request, 'deleteDes.html', {
        'id_user': id_user, 
        'despesas': despesas['itens'],
        'status': status,
        'qnt': qnt
        }
    )

def validaDeleteDes(request):
    id_user = request.session['user']['id']
    deletes = pegaSelecoesDelete(request.POST, id_user, despesasDB)
    
    if len(deletes) > 0:
        deleteDB(deletes, despesasDB, id_user)
    else:
        return redirect('/despesas/deleteDes/?status=1')
    
    return redirect('/despesas/deleteDes/?status=0')
