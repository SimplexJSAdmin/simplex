from django.shortcuts import render
import requests
from django.http import HttpResponse
from .functions import *
from .models import *
import pandas as pd

# Create your views here.
def home(request):
    #TODO: Primero guardar el log de back2 ocupado
    #TODO: Establecer logica para cargar los archivos
    if request.method == 'POST':
       planta = request.FILES['planta']
       print(planta)
    return HttpResponse('inicio')



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