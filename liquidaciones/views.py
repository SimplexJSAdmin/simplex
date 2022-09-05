from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.shortcuts import render, redirect
from .models import Empresa, EmpresasPermitidas, Planta, ParametrosEPS, ParametrosFSP, ParametrosAFP, ParametrosARL, ParametrosCAJA, ParametrosICBF, ParametrosSENA, ConceptoEmpresa, ConceptoInterno
from .forms import  *
from .decorators import *
from .functions import *


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
    if request.method == 'POST':
        id_empresa = request.POST['empresa_plataforma']
        request.session['id_empresa'] = id_empresa
        print(id_empresa)
        messages.success(request, 'Empresa seleccionada con éxito, ahora puedes usar los módulos')
        return redirect('inicio')
    empresas_permitidas = EmpresasPermitidas.objects.filter(id_usuario = request.user.id)
    print(empresas_permitidas)
    modules = get_modules(request)
    return render(request, "index.html", {'modules': modules, 'url_name': 'inicio', 'empresas_permitidas': empresas_permitidas})


@login_required(login_url='login')
@allowed_users(['reportes'])
def obtener_reportes_opciones(request):
    modules = get_modules(request)
    opciones_reporte = {'nomina': 'Nómina', 'planta': 'Planta', 'liquidaciones': 'Liquidaciones'}
    return render(request, 'reportes/obtener_reportes.html', {'opciones': opciones_reporte, 'modules': modules, 'url_name': 'reportes'} )


@login_required(login_url='login')
@allowed_users(['reportes'])
def obtener_reportes_final(request):
    modules = get_modules(request)
    if request.method == 'POST':
        tipo_reporte = request.POST['tipo_reporte']
    else:
        return redirect('home_reportes')
    return render(request, 'reportes/resultado.html', {'opcion': tipo_reporte, 'modules': modules, 'url_name': 'reportes'})


@login_required(login_url='login')
@allowed_users(['preprocesamiento'])
def preprocesamiento_home(request):
    modules = get_modules(request)
    return render(request, 'preprocesamiento/preprocesamiento_home.html', {'modules': modules, 'url_name': 'preprocesamiento'})


@login_required(login_url='login')
@allowed_users(['liquidaciones'])
def liquidaciones_home(request):
    modules = get_modules(request)
    return render(request, 'liquidaciones/liquidaciones_home.html', {'modules': modules, 'url_name': 'liquidaciones'})


"""Inicio de vistas de parametros"""
@login_required(login_url='login')
@allowed_users(['parametros'])
def parametros_home(request):
    print(request.session['id_empresa'])
    modules = get_modules(request)
    return render(request, 'parametros/parametros_home.html', {'modules': modules, 'url_name': 'parametros'})


@login_required(login_url='login')
@allowed_users(['parametros'])
def parametros_list(request, parameter_type):
    modules = get_modules(request)
    context = {'modules': modules, 'url_name': 'parametros', 'parameter_type': parameter_type}
    tablas_topes = {'eps': ParametrosEPS, 'afp': ParametrosAFP, 'fsp': ParametrosFSP, 'sena': ParametrosSENA, 'icbf': ParametrosICBF}
    if parameter_type == 'arl':
        parametros = ParametrosARL.objects.all()
        context.update({'parametros': parametros, 'tabla_riesgos': True})
    elif parameter_type == 'caja':
        parametros = ParametrosCAJA.objects.all()
        context.update({'parametros': parametros, 'tabla_basica': True})
    elif parameter_type in tablas_topes:
        parametros = tablas_topes[parameter_type].objects.all()
        context.update({'parametros': parametros, 'tabla_topes': True})
    else:
        return redirect('parametros')
    return render(request, 'parametros/parametros_lista.html', context)

"""fin de vistas de parametros"""

""" Vistas relacionadas con conceptos internos y de empresa"""
@login_required(login_url='login')
@allowed_users(['conceptos'])
def conceptos_home(request):
    conceptos_empresa = ConceptoEmpresa.objects.filter(empresa_id=request.session['id_empresa'])
    #concepto_empresa = conceptos_empresa[0]
    #print(concepto_empresa.__dict__)
    modules = get_modules(request)
    return render(request, 'conceptos/conceptos_home.html', {'modules': modules, 'url_name': 'conceptos', 'conceptos_empresa':conceptos_empresa})

@login_required(login_url='login')
@allowed_users(['conceptos'])
def conceptos_internos_home(request):
    modules = get_modules(request)
    conceptos_internos = ConceptoInterno.objects.all()
    return render(request, 'conceptos/internos/conceptos_internos_home.html', {'url_name':'conceptos', 'conceptos_internos':conceptos_internos, 'modules':modules})

@login_required(login_url='login')
@allowed_users(['conceptos'])
def conceptos_internos_crear(request):
    formulario = ConceptoInternoForm(request.POST or None)
    return render(request, 'conceptos/internos/conceptos_internos_crear.html', {'formulario':formulario})


"""Fin de vistas de conceptos internos y de empresa"""

@login_required(login_url='login')
@allowed_users(['informes'])
def informes_home(request):
    modules = get_modules(request)
    return render(request, 'informes/informes_home.html', {'modules': modules, 'url_name': 'informes'})

@login_required(login_url='login')
@allowed_users(['logs'])
def logs_home(request):
    modules = get_modules(request)
    return render(request, 'logs/logs_home.html', {'modules': modules, 'url_name': 'logs'})


"""
    Vistas relacionadas con el modulo empresa
"""
@login_required(login_url='login')
@allowed_users(['empresas'])
def empresas_home(request):
    empresas  = Empresa.objects.all()
    modules = get_modules(request)
    return render(request, 'empresas/empresas_home.html', {'modules': modules, 'url_name': 'empresas', 'empresas': empresas})

@login_required(login_url='login')
@allowed_users(['empresas'])
def empresas_crear(request):
    modules = get_modules(request)
    formulario = EmpresasCreateForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('empresas')
    return render(request, 'empresas/empresa_crear.html', {'modules': modules, 'url_name': 'empresas', 'formulario': formulario})


"""
Fin modulo de empresas
"""

@login_required(login_url='login')
def logout(request):
    try:
        del(request.session['id_empresa'])
    except:
        pass
    if request.user.is_authenticated:
        logout_django(request)
    return redirect('login')