from django.shortcuts import render, redirect
from .models import Parametro, Empleado
from .forms import ParametroForm

def inicio(request):
    return render(request, "paginas/home.html")

def lista_parametros(request):
    parametros = Parametro.objects.all()
    return render(request, 'paginas/lista_parametros.html', {'parametros': parametros})

def creacion_parametros(request):
    formulario = ParametroForm(request.POST or None)
    if(formulario.is_valid()):
        formulario.save()
        return redirect('lista_parametros')
    return render(request, 'paginas/crear_parametro.html', {'formulario':formulario})

def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'paginas/empleados.html', {'empleados':empleados})

def eliminar_parametro(request, id):
    parametro = Parametro.objects.get(id=id)
    parametro.delete()
    return redirect('lista_parametros')

def editar_parametro(request, id):
    parametro = Parametro.objects.get(id=id)
    formulario = ParametroForm(request.POST or None, instance=parametro)
    if(formulario.is_valid() and request.POST):
        formulario.save()
        return redirect('lista_parametros')
    return render(request, 'paginas/editar_parametro.html', {'formulario':formulario})