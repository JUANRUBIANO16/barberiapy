

from django.urls import path

from .import views


urlpatterns = [

path('servicios/',views.lista_servicios, name='listar_servicios'),

]