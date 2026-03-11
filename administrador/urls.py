



from django.urls import path

from administrador import views


urlpatterns =[
 path("",views.dashboard,name='dashboard')
]



