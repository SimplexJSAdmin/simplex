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
from datetime import datetime
from .model_v2 import Model
from time import time


def login_back_2(request):
    login_form = LoginForm(request.POST or None)
    context = {'form': login_form}
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
        dataframe_planta = pd.read_csv(io.StringIO(planta.read().decode('utf-8')), delimiter=';', dtype='string')
        dataframe_nomina = pd.read_csv(io.StringIO(nomina.read().decode('utf-8')), delimiter=';', dtype='string')
        dataframe_novedades = pd.read_csv(io.StringIO(novedades.read().decode('utf-8')), delimiter=',')
        dataframe_planta.to_csv('/code/archivos_origen/planta'+get_periodo_actual()['cod'], index = False)
        dataframe_nomina.to_csv('/code/archivos_origen/nomina'+get_periodo_actual()['cod'], index = False)
        dataframe_novedades.to_csv('/code/archivos_origen/novedades'+get_periodo_actual()['cod'], index = False)
        return HttpResponse('Archivos recibidos y cargados con exito')
    return render(request, 'cargar_archivos.html', context)


def cargar(request, periodo, empresa):
    cliente = login()
    print('Etapa de logeo pasada')
    preprocesamiento_creado = Preprocesamiento.objects.filter(periodo_id=periodo,
                                                              empresa_id=empresa)
    url = 'http://172.21.0.4:8000/app/preprocesamiento/descargar/nomina/' + str(preprocesamiento_creado[0].nomina)
    file = cliente.get(url, timeout=10)
    print("Archivo obtenido:", file)
    logout(cliente)
    return HttpResponse('Resultado obtenido')



@login_required()
def liquidar(request):
    context = {}
    periodo = request.Session['periodo']
    global id_empresa
    id_empresa = request.Session['id_empresa']
    if request.method == 'POST':
        current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')

        a = time()

        api = Model('Sicard', 2022, 8)
        info = api.generar_liquidacion(
            # TEST 1
            # Nomina_actual='./test/nomina_junio.csv',
            # Nomina_anterior='./test/nomina_junio.csv',
            # Planta_actual='./test/planta_junio.csv',
            # Planta_anterior='./test/planta_junio.csv',
            # Liquidacion_actual='./test/liquidacion_junio.csv',
            # Liquidacion_anterior='./test/liquidacion_junio.csv',
            #
            # TEST 2
            Nomina_actual= request.POST['nomina_actual'],
            Nomina_anterior= request.POST['nomina_anterior'],
            Planta_actual= request.POST['planta_actual'],
            Planta_anterior= request.POST['planta_anterior'],
            Liquidacion_actual= request.POST['liquidacion_actual'],
            Liquidacion_anterior= request.POST['liquidacion_anterior'],
            #
            # TEST 3
            # Nomina_actual='./test/nomina_julio.csv',
            # Nomina_anterior='./test/nomina_julio.csv',
            # Planta_actual='./test/planta_julio.csv',
            # Planta_anterior='./test/planta_julio.csv',
            # Liquidacion_actual='./test/liquidacion_julio.csv',
            # Liquidacion_anterior='./test/liquidacion_julio.csv',
            PATH=f'/code/liquidaciones/{current_datetime}_agosto.csv'
        )

        b = time()

        t1 = b - a
        t2 = (b - a) / 60
        t3 = ((b - a) / 18) * 6000
        t4 = (((b - a) / 18) * 6000) / 60

        print('\n\n -> Tiempo estimado de ejecución: {:.2f}s ~ {:.2f}m'.format(t1, t2))
        return HttpResponse('El proceso ha finalizado')
    return render (request, 'iniciar_proceso.html', context)