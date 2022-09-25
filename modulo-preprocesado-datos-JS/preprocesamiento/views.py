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
    file_nomina = ()
    file_planta = ()
    file_novedades = ()
    logs = Log.objects.all()
    empresas = Empresa.objects.all()
    #TODO: Al finalizar escribir log de proceso finalizado
    return render(request, 'empresa_prueba.html', {'empresas':logs})

def cargar(request, periodo, empresa):
    cliente = login()
    print('Etapa de logeo pasada')
    preprocesamiento_creado = Preprocesamiento.objects.filter(periodo_id=periodo,
                                                              empresa_id=empresa)
    file = cliente.get('http://localhost:8001/app/preprocesamiento/descargar/nomina/'+preprocesamiento_creado[0].nomina, timeout=10)
    print(file)
    logout(cliente)
    return HttpResponse(request,'Resultado obtenido')

def liquidar(request):
    pass