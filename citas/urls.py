

from django.urls import path
from .import views
urlpatterns = [

    path('',views.citas, name="citas"),
    path('crear/',views.crearCita,name='crear_Cita') ,
    path('edit/<int:id>',views.cita_edit,name='cita_edit') ,  
    path('delete/<int:id>',views.cita_delete,name='cita_delete') ,
    
]