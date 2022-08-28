from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient
from hashlib import sha256

from .cadastro import db

def excluirConta(request):
    id_user = request.session['user']['id']
    operaExclusao(id_user)
    request.session['user'] = None
    return redirect('/user/login/?status=2')


def operaExclusao(id_user):
    colecoes = ['despesas', 'categories', 'poupanca']
    for i in colecoes:
        db[i].find_one_and_delete({'id_user': id_user})
    
    db['users'].find_one_and_delete({'id': id_user})

    control = db['users'].find_one({'id': 0})
    control['counter'] = control['counter'] - 1

    db['users'].update_one(
        {'id': 0},
        {"$set": control}
    )