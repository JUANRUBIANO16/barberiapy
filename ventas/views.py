from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ventas.models import Venta
from citas.models import Cita
from barberia.decorators import login_required

@login_required
def ventas(request):
    """
    Muestra las ventas según el rol:
    - Admin: todas las ventas
    - Barbero: solo sus ventas asociadas a sus citas
    """
    user_id = int(request.session.get('user_id'))
    rol = request.session.get('user_rol')

    if rol == 'admin':
        ventas_qs = Venta.objects.all()
    else:  # barbero
        # Solo ventas de las citas de este barbero
        citas_barbero = Cita.objects.filter(barbero_id=user_id)
        ventas_qs = Venta.objects.filter(cita_id__in=citas_barbero.values_list('id', flat=True))

    ventas_totales = ventas_qs.count()
    citas = Cita.objects.all()  # se puede filtrar también si quieres solo las del barbero

    return render(request, 'ventas.html', {
        'ventas': ventas_qs,
        'citas': citas,
        'ventas_totales': ventas_totales
    })


@login_required
def crearVenta(request):
    """
    Crea una venta asociada a una cita.
    """
    if request.method == 'POST':
        try:
            cita_id = request.POST.get('cita')
            subtotal = Decimal(request.POST.get('subtotal'))
            descuento = Decimal(request.POST.get('descuento') or '0')

            cita = get_object_or_404(Cita, id=cita_id)

            total = subtotal - descuento

            Venta.objects.create(
                cita=cita,
                subtotal=subtotal,
                descuento=descuento,
                total=total
            )

            messages.success(request, "Venta registrada correctamente")

        except (InvalidOperation, ValueError):
            messages.error(request, "El valor ingresado es inválido o demasiado grande")

    return redirect('ventas')


@login_required
def venta_edit(request, id):
    """
    Edita una venta existente.
    """
    venta = get_object_or_404(Venta, id=id)

    if request.method == 'POST':
        try:
            cita_id = request.POST.get('cita')
            subtotal = Decimal(request.POST.get('subtotal'))
            descuento = Decimal(request.POST.get('descuento') or '0')

            venta.cita = get_object_or_404(Cita, id=cita_id)
            venta.subtotal = subtotal
            venta.descuento = descuento
            venta.total = subtotal - descuento
            venta.save()

            messages.success(request, "Venta actualizada correctamente")

        except (InvalidOperation, ValueError):
            messages.error(request, "Número inválido o demasiado grande")

    return redirect('ventas')


@login_required
def venta_delete(request, id):
    """
    Elimina una venta.
    """
    venta = get_object_or_404(Venta, id=id)
    venta.delete()
    messages.success(request, "Venta eliminada correctamente")

    return redirect('ventas')