from django.http import HttpResponse
from django.shortcuts import redirect, render


def cadastrarDes(request):
    return render(request, 'cadastrarDes.html')