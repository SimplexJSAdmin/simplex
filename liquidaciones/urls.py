from django.urls import path
from . import views

urlpatterns = [
    path('home', views.inicio, name='inicio'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('reportes', views.obtener_reportes_opciones, name='home_reportes'),
    path('reportes/resultado', views.obtener_reportes_final, name='reportes_result')
]
