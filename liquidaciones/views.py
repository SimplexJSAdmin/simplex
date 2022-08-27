from django.shortcuts import render
from .models import Empresa, Planta

# Create your views here.

def inicio(request):
    return render(request, "index.html")

def obtener_reportes_opciones(request):
    opciones_reporte = {'nomina':'Nómina', 'planta':'Planta', 'liquidaciones':'Liquidaciones'}
    return render(request, 'reportes/obtener_reportes.html', {'opciones':opciones_reporte} )

def obtener_reportes_final(request, opcion):
    return render(request, 'reportes/resultado.html', {'opcion':opcion})

