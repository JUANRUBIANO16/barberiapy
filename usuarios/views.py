from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from usuarios.models import Usuario
from django.contrib.auth.hashers import make_password
from barberia.decorators import login_required, role_required


@role_required('admin')
def usuario_list(request):
    """
    Lista todos los usuarios para el administrador.
    """
    usuarios = Usuario.objects.all()
    total_usuarios = Usuario.objects.count()
    return render(request, 'usuarios.html', {
        'usuarios': usuarios,
        'total_usuarios': total_usuarios
    })


def usuario_create(request):
    """
    Crear un usuario nuevo, validando datos y guardando foto.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo_usuario = request.POST.get('tipo_usuario')
        foto = request.FILES.get('foto')  # <-- aquí capturamos la foto

        # Validaciones
        if not password or len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return redirect('usuarios')

        if Usuario.objects.filter(nombre=nombre).exists():
            messages.error(request, 'Este nombre ya está en uso')
            return redirect('usuarios')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado')
            return redirect('usuarios')

        # Crear el usuario
        Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password=make_password(password),
            tipo_usuario=tipo_usuario,
            foto=foto
        )

        messages.success(request, 'Usuario creado correctamente')
        return redirect('usuarios')


def usuario_edit(request, id):
    """
    Editar un usuario existente, incluyendo foto y contraseña opcional.
    """
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo_usuario = request.POST.get('tipo_usuario')
        foto = request.FILES.get('foto')  # <-- nueva foto

        # Validaciones
        if Usuario.objects.filter(nombre=nombre).exclude(id=id).exists():
            messages.error(request, 'Este nombre ya está en uso')
            return redirect('usuarios')

        if Usuario.objects.filter(email=email).exclude(id=id).exists():
            messages.error(request, 'Este correo ya está en uso')
            return redirect('usuarios')

        if password and len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return redirect('usuarios')

        # Guardar cambios
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.email = email
        usuario.tipo_usuario = tipo_usuario

        if password:
            usuario.password = make_password(password)

        if foto:
            usuario.foto = foto

        usuario.save()
        messages.success(request, 'Usuario actualizado correctamente')
        return redirect('usuarios')


def usuario_delete(request, id):
    """
    Elimina un usuario.
    """
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente')

    return redirect('usuarios')