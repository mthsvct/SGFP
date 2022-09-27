from django.http import HttpResponse
from django.shortcuts import redirect, render
from datetime import date

from categories.views import pegaCategorias
from .despesas import despesasDB

STATUS_DESPESA = {
    1: {
        'descricao': 'Pago',
        'cor': 'green'
    },
    2: {
        'descricao': 'Em andamento',
        'cor': 'yellow'
    },
    3: {
        'descricao': 'Atrasado',
        'cor': 'red'
    }
}

def cadastrarDes(request):
    user = request.session.get('user')
    categorias = pegaCategorias(user['id'])
    hoje = date.today().strftime('%Y-%m-%d')
    status = request.GET.get('status')
    return render(request, 'cadastrarDes.html', {'categorias': categorias, 'hoje': hoje, 'status': status})

def validaCadDes(request):

    name = request.POST['name']
    des = request.POST['description']
    valor = request.POST['valor']
    vencimento = request.POST['vencimento']
    cat = int(request.POST['categoria'])
    id_user = request.session['user']['id']

    salvar_des_BD(name, des, valor, vencimento, cat, id_user)
    
    return redirect('/despesas/cadastrarDes/?status=0')

def salvar_des_BD(name, des, valor, vencimento, cat, id_user):
    # Salva uma nova despesa no banco de dados.
    col = despesasDB.find_one({'id_user': id_user})

    col['itens'].append(
        {
            'id': col['control']['last_id'] + 1,
            'name': name,
            'description': des,
            'valor': {
                'completo': float(valor),
                'restante': float(valor),
                'pago': float(0)
            },
            'vencimento': vencimento,
            'categoria': cat,
            'id_user': id_user,
            'status': pegaStatus(vencimento),
            'repete': {}, # se essa despesa se repetir, deve ser por inicialmente: dia, semana, mês
            'pagamento': [] # Aqui pode ser uma lista de objetos com pagamento.
            
        }
    )
    
    atualizaControlItens(col)

    despesasDB.update_one(
        {'id_user': id_user}, 
        {"$set": col}
    ) # Atualiza

def montaData(vencimento):
    separado = vencimento.split('-')
    data = date(
        int(separado[0]),
        int(separado[1]),
        int(separado[2]),
    ) # Montei a data a partir da string vinda do formulário.
    return data

def pegaStatus(vencimento):
    data = montaData(vencimento)
    hoje = date.today()
    dias = data - hoje

    if dias.days > -1:
        retorno = 2
    else:
        retorno = 3

    return retorno


def atualizaControlItens(collection):
    # Este atualiza as collections de Despesas e Categorias
    collection['control']['counter'] = len(collection['itens'])
    collection['control']['last_id'] = collection['control']['last_id'] + 1

