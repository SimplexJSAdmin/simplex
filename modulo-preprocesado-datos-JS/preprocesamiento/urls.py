
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('cargar-registros-bd/<int:periodo>/<int:empresa>', views.cargar, name='cargar'),
    path('login/', views.login_back_2, name='login'),
    path('iniciar/', views.liquidar, name='cargar')
]