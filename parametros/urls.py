from django.urls import path
from . import views

urlpatterns = [
    path('home', views.inicio, name='inicio_parametros'),
    path('', views.lista_parametros, name='lista_parametros'),
    path('crear/', views.creacion_parametros, name='crear_parametro'),
    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('eliminar/<int:id>', views.eliminar_parametro, name='eliminar_parametro'),
    path('editar/<int:id>', views.editar_parametro, name='editar_parametro')
]