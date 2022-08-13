from django.http import HttpResponse
from django.shortcuts import redirect, render


def deleteDes(request):
    return render(request, 'deleteDes.html')