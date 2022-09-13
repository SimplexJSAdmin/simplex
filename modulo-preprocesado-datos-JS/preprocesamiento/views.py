from django.shortcuts import render
from .models import *
import pandas as pd
from functions import *

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
