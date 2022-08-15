from django.http import HttpResponse
from django.shortcuts import redirect, render

from .despesas import despesasDB
from categories.views import pegaSelecoesDelete, deleteDB

def deleteDes(request):
    id_user = request.session['user']['id']
    despesas = list(despesasDB.find({'id_user': id_user}))
    status = request.GET.get('status')
    qnt = len(despesas)
    return render(request, 'deleteDes.html', {
        'id_user': id_user, 
        'despesas': despesas,
        'status': status,
        'qnt': qnt
        }
    )

def validaDeleteDes(request):
    deletes = pegaSelecoesDelete(request.POST, request.session['user']['id'], despesasDB)
    
    if len(deletes) > 0:
        deleteDB(deletes, despesasDB)
    else:
        return redirect('/despesas/deleteDes/?status=1')
    
    return redirect('/despesas/deleteDes/?status=0')
