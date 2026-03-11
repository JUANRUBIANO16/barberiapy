from django.shortcuts import render



def comprobante(request):
    return render(request,"comprobantes.html")
