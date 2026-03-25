from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from usuarios.models import Usuario
from django.contrib.auth.hashers import make_password

#aca la vista para listar los usuarios con su contexto para mostrar en la plantilla
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})


def usuario_create(request):
# si el requets que llega es post procedemos a capturar los datos del formulario
    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo_usuario = request.POST.get('tipo_usuario')
      # aqui se valida que la contraseña tenga al menos 6 caracteres
        if not password or len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return redirect('usuarios')
        #aqui se valida que ai el correo ya existe en la base de datos para evitar duplicados
        
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado')
            return redirect('usuarios')

# si todo es correcto se crea el usuario y devolvemos un mensaje de éxito y redirigimos a la lista de usuarios
        Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password=make_password(password),
            tipo_usuario=tipo_usuario
        )

        messages.success(request, 'Usuario creado correctamente')
        return redirect('usuarios')


def usuario_edit(request, id):
    # Obtenemos el usuario
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        # Datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')  
        tipo_usuario = request.POST.get('tipo_usuario')

        # Validar correo único
        if Usuario.objects.filter(email=email).exclude(id=id).exists():
            messages.error(request, 'Este correo ya está en uso')
            return redirect('usuarios')

        # Validar password si se ingresó
        if password and len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return redirect('usuarios')

        # Guardamos los datos
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.email = email
        usuario.tipo_usuario = tipo_usuario

        # Solo actualizamos la contraseña si se ingresó
        if password:
            usuario.password = make_password(password)

        usuario.save()
        messages.success(request, 'Usuario actualizado correctamente')
        return redirect('usuarios')