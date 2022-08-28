from datetime import date
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

    if c['qnt'] > 0:
        return redirect('/user/cadastro/?status=1')
        
    cadastroBD(name, email, password)

    return redirect('/user/login/?status=0')

def buscaRepetido(email):
    # Retorna a quantidade de contas e a conta que possui aquele email, se for encontrado.
    b = users.find({'email':email})
    buscado = len(list(b))

    if buscado == 0:
        retorno = {'qnt': buscado, 'user': None}
    else:
        retorno = {'qnt': buscado, 'user': b[0]}

    return retorno

def atualizaControl(collection):
    c = collection.find_one({"id": 0})
    counter = c['counter'] + 1
    last_id = c['last_id'] + 1
    collection.update_one({'id': 0}, {"$set":{'counter': counter, 'last_id': last_id}})

def cadastroBD(name, email, password):
    c = users.find_one({"id": 0})
    user = {
        'id': c['last_id'] + 1,
        'name': name,
        'email': email,
        'password': sha256(password.encode()).hexdigest(),
        'renda': {
            'saldo': float(0),
            'renda_mensal': float(0),
            'data': date.today().strftime("%Y-%m-%d")
        }
    }
    users.insert_one(user)
    cadUser(user['id'])

def cadUser(id_user):
    atualizaControl(users)
    cadUserCategorie(id_user)
    cadUserDespesas(id_user)
    cadUserPoupanca(id_user)

def cadUserDespesas(id_user):
    d = {
        "id_user": id_user,
        "control": {
            "counter": 0,
            "last_id": 0,
        },
        "itens": []
    }
    db['despesas'].insert_one(d)

def cadUserPoupanca(id_user):
    hoje = date.today()
    p = {
        'id_user': id_user,
        'planejado': float(0), # valor que se pretende alcançar.
        'data': {
            'meses': 0,
            'data': hoje.strftime('%Y-%m-%d')
        },  # data calculada que será levada para alcançar o valor.
        'guardado': float(0), # Valor que já se encontra na poupanca
        'mensal': float(0) # valor a ser guardado todo mês
    }
    db['poupanca'].insert_one(p)

def cadUserCategorie(id_user):
    cat = {
        "id_user": id_user,
        "control": {
            "counter": 8,
	        "last_id": 8,
        },
        "itens": [ 
            {
                "id": 1,
                "name": "Super-Mercado",
                "description": "Comida, limpeza, produtos",
                "color": "#ffff87"
            },{
                "id": 2,
                "name": "Aluguel",
                "description": "Moradia",
                "color": "#ffff87"
            },{
                "id": 3,
                "name": "Energia",
                "description": "Conta de Luz",
                "color": "#ffff87"
            },{
                "id": 4,
                "name": "Combustivel",
                "description": "Gasto em Combustivel",
                "color": "#ffff87"
            },{
                "id": 5,
                "name": "Internet",
                "description": "Internet",
                "color": "#ffff87"
            },{
                "id": 6,
                "name": "Água",
                "description": "Água",
                "color": "#ffff87"
            },{
                "id": 7,
                "name": "Gás",
                "description": "Gás",
                "color": "#ffff87"
            },{
                "id": 8,
                "name": "Transporte Público",
                "description": "Transporte Público",
                "color": "#ffff87"
            }
	    ]
    }
    db['categories'].insert_one(cat)