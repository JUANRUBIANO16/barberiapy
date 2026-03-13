

from django.shortcuts import render

from usuarios.models import Usuario


def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request,'usuarios.html', {'usuarios': usuarios})

