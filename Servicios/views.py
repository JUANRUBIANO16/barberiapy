from django.shortcuts import render

from Servicios.models import Servicio



def lista_servicios(request):

    servicios=Servicio.objects.all()
    return render(request, 'servicios.html', {'servicios': servicios})