from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.shortcuts import render, redirect
from .models import Empresa, Planta
from .decorators import *


@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['pass']
        user = authenticate(username=username, password=passwd)
        if user is not None:
            login_django(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Credenciales invalidas')
    return render(request, 'login.html')



@login_required(login_url='login')
def inicio(request):
    return render(request, "index.html")


@login_required(login_url='login')
@allowed_users(['preprocesado'])
def obtener_reportes_opciones(request):
    opciones_reporte = {'nomina':'Nómina', 'planta':'Planta', 'liquidaciones':'Liquidaciones'}
    return render(request, 'reportes/obtener_reportes.html', {'opciones':opciones_reporte} )


@login_required(login_url='login')
@allowed_users(['reportes'])
def obtener_reportes_final(request):
    if request.method == 'POST':
        tipo_reporte = request.POST['tipo_reporte']
    else:
        return redirect('home_reportes')
    return render(request, 'reportes/resultado.html', {'opcion':tipo_reporte})

@login_required(login_url='login')
def logout(request):
    if request.user.is_authenticated:
        logout_django(request)
    return redirect('login')