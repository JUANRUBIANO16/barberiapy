from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from citas.models import Cita
from Servicios.models import Servicio
from usuarios.models import Usuario
from barberia.decorators import login_required, role_required


#aca listamos todos los contextos necesarios para mostrar en la plantilla de citas
@login_required
def citas(request):
    user_id = request.session.get('user_id')
    rol = request.session.get('user_rol')

    
    if rol == 'admin':
        lista_citas = Cita.objects.all()
    elif rol == 'barbero':
        lista_citas = Cita.objects.filter(barbero_id=user_id)
    else:
        lista_citas = Cita.objects.none()

    return render(request, "citas/citas.html", {
        'citas': lista_citas,
        'barberos': Usuario.objects.filter(tipo_usuario='barbero'),
        'clientes': Usuario.objects.filter(tipo_usuario='cliente'),
        'servicios': Servicio.objects.all(),
        'estados': Cita.ESTADOS
    })
def crearCita(request):
    if request.method == 'POST':

        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        estado = request.POST.get('estado')

        barbero_id = request.POST.get('barbero')
        cliente_id = request.POST.get('cliente')
        servicio_id = request.POST.get('servicio')

        try:
            # validación correcta
            barbero = Usuario.objects.get(id=barbero_id, tipo_usuario='barbero')
            cliente = Usuario.objects.get(id=cliente_id, tipo_usuario='cliente')
            servicio = Servicio.objects.get(id=servicio_id)
        except:
            messages.error(request, 'Datos inválidos')
            return redirect('citas')

        # evitar doble cita
        if Cita.objects.filter(
            fecha=fecha,
            hora=hora,
            barbero=barbero
        ).exists():
            messages.error(request, 'El barbero ya tiene una cita en esa hora')
            return redirect('citas')

        Cita.objects.create(
            fecha=fecha,
            hora=hora,
            estado=estado,
            barbero=barbero,
            cliente=cliente,
            servicio=servicio,
        )

        messages.success(request, 'Cita creada correctamente')
        return redirect('citas')

    return redirect('citas')


def cita_edit(request, id):
    cita = get_object_or_404(Cita, id=id)

    if request.method == 'POST':

        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        estado = request.POST.get('estado')

        try:
            barbero = Usuario.objects.get(id=request.POST.get('barbero'), tipo_usuario='barbero')
            cliente = Usuario.objects.get(id=request.POST.get('cliente'), tipo_usuario='cliente')
            servicio = Servicio.objects.get(id=request.POST.get('servicio'))
        except:
            messages.error(request, 'Datos inválidos')
            return redirect('citas')

        if Cita.objects.filter(
            fecha=fecha,
            hora=hora,
            barbero=barbero
        ).exclude(id=id).exists():
            messages.error(request, 'El barbero ya tiene otra cita en esa hora')
            return redirect('citas')

        cita.fecha = fecha
        cita.hora = hora
        cita.estado = estado
        cita.barbero = barbero
        cita.cliente = cliente
        cita.servicio = servicio

        cita.save()

        messages.success(request, 'Cita actualizada correctamente')
        return redirect('citas')

    return redirect('citas')



def cita_delete(request, id):
    cita=get_object_or_404(Cita,id=id)
    cita.delete()
    
    messages.success(request, 'Cita eliminada correctamente')
    return redirect('citas')