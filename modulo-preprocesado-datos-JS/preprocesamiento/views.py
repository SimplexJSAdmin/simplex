from django.shortcuts import render
import requests, io
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .functions import *
from .models import *
from .forms import *
import pandas as pd


def login_back_2(request):
    login_form = LoginForm(request.POST or None)
    context = {'form':login_form}
    if request.method == 'POST':
        if login_form.is_valid():
            user = request.POST['user']
            passwd = request.POST['passwd']
            user = authenticate(username=user, password=passwd)
            if user is not None:
                login(request, user)
                return HttpResponse('Usuario autenticado con exito')
            else:
                return HttpResponse('Error al autenticar')
    return render(request, 'login.html', context)




@login_required(login_url='login')
def home(request):
    context = {}
    form_files = FilesForm(request.POST or None)
    context.update({'form': form_files})
    if request.method == 'POST':
        planta = request.FILES['planta']
        nomina = request.FILES['nomina']
        novedades = request.FILES['novedades']
        dataframe_planta = pd.read_csv(io.StringIO(planta.read().decode('utf-8')), delimiter=',')
        dataframe_nomina = pd.read_csvl(io.StringIO(nomina.read().decode('utf-8')), delimiter=',')
        #dataframe_novedades = pd.read_csv(io.StringIO(novedades.read().decode('utf-8')), delimiter=',')
        print(dataframe_planta)
        print(nomina)
        print(novedades)
        return HttpResponse('Archivos recibidos con exito')
    return render(request, 'cargar_archivos.html', context)



def cargar(request, periodo, empresa):
    cliente = login()
    print('Etapa de logeo pasada')
    preprocesamiento_creado = Preprocesamiento.objects.filter(periodo_id=periodo,
                                                              empresa_id=empresa)
    url = 'http://172.21.0.4:8000/app/preprocesamiento/descargar/nomina/'+str(preprocesamiento_creado[0].nomina)
    file = cliente.get(url, timeout=10)
    print("Archivo obtenido:", file)
    logout(cliente)
    return HttpResponse('Resultado obtenido')

def liquidar(request):
    pass