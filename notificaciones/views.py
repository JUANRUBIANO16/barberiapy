from django.shortcuts import redirect, render
from notificaciones.models import SolicitudCita
from Servicios.models import Servicio


def notificaciones(request):
    notificaciones = SolicitudCita.objects.all()
    servicios = Servicio.objects.all()

    return render(request, "notificaciones.html", {
        'notificaciones': notificaciones,
        'servicios': servicios
    })


def editar_notificacion(request, id):
    try:
        notificacion = SolicitudCita.objects.get(id=id)

        if request.method == 'POST':
            notificacion.nombre = request.POST.get('nombre')
            notificacion.telefono = request.POST.get('telefono')
            notificacion.email = request.POST.get('email')
            notificacion.mensaje = request.POST.get('mensaje')

            servicio_id = request.POST.get('servicio')
            if servicio_id:
                notificacion.servicio = Servicio.objects.filter(id=servicio_id).first()
            else:
                notificacion.servicio = None

            notificacion.save()

    except SolicitudCita.DoesNotExist:
        pass

    return redirect('notificaciones')


def eliminar_notificacion(request, id):
    try:
        notificacion = SolicitudCita.objects.get(id=id)
        notificacion.delete()
    except SolicitudCita.DoesNotExist:
        pass

    return redirect('notificaciones')


# ✅ aceptar solicitud
def aceptar_cita(request, id):
    try:
        notificacion = SolicitudCita.objects.get(id=id)
        notificacion.estado = 'aceptada'
        notificacion.save()
    except SolicitudCita.DoesNotExist:
        pass

    return redirect('notificaciones')


# ✅ cancelar solicitud
def cancelar_cita(request, id):
    try:
        notificacion = SolicitudCita.objects.get(id=id)
        notificacion.estado = 'cancelada'
        notificacion.save()
    except SolicitudCita.DoesNotExist:
        pass

    return redirect('notificaciones')