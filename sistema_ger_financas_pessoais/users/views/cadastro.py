from django.shortcuts import redirect, render
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient
from hashlib import sha256
# Create your views here.

# db é o banco de dados do mongoDB
# users é a collection referentes aos usuários
db = MongoClient('mongodb+srv://matheusV:Z6ds6qWoyRc35cia@sisgerfinp.tlmph32.mongodb.net/?retryWrites=true&w=majority')['sisGerFinP']
users = db['users']


def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})


def validaCadastro(request):
    # [  ] - Fazer a busca para ver se já não há algum usuário com o mesmo email que está tentando se cadastrar
    name = request.POST['userName']
    email = request.POST['email']
    password = request.POST['password']

    c = buscaRepetido(email)

    if c > 0:
        return redirect('/user/cadastro/?status=1')
        
    cadastroBD(name, email, password)

    return redirect('/user/login/?status=0')
  

def buscaRepetido(email):
    b = users.find({'email':email})
    buscado = len(list(b))
    return buscado


def cadastroBD(name, email, password):
    count = users.count_documents({})
    user = {
        'id': int(count)+1,
        'name': name,
        'email': email,
        'password': sha256(password.encode()).hexdigest(),
        'renda': float(0)
    }
    users.insert_one(user)

