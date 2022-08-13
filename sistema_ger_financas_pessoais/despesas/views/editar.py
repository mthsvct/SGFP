from django.http import HttpResponse
from django.shortcuts import redirect, render


def editarDes(request):
    return render(request, 'editarDes.html')