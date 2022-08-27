from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('reportes', views.obtener_reportes_opciones, name='home_reportes'),
    path('reportes/<str:opcion>', views.obtener_reportes_final, name='reportes_result')
]
