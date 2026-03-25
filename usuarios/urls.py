from django.urls import path

from .import views


urlpatterns = [

    path('',views.usuario_list, name="usuarios"),
    path('crear/',views.usuario_create,name='crear_usuarios'),
    path('edit/<int:id>',views.usuario_edit,name='editar_usuarios')
]


