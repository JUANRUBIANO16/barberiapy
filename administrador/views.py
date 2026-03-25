from urllib import request

from django.shortcuts import render



def dashboard(request):

    return render(request,"administrador/dashboard.html")


def perfiles(request):

    return render(request,"administrador/perfil.html")