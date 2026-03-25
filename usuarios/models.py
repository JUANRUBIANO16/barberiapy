from django.db import models

class Usuario(models.Model):
    TIPO_USUARIO = [
        ('admin', 'Admin'),
        ('barbero', 'Barbero'),
        ('cliente', 'Cliente'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO)

    def __str__(self):
        return self.nombre