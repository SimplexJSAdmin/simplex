import re
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from .models import Empresa, EmpresasPermitidas, Planta, ParametrosEPS, ParametrosFSP, ParametrosAFP, ParametrosARL, ParametrosCAJA, ParametrosICBF, ParametrosSENA, ConceptoEmpresa, ConceptoInterno, Log
from .forms import  *
from .decorators import *
from .functions import *
from .filters import LogsFilter


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
        resultados = Nomina.objects.all()
        myFilter = ReportFilter(request.GET, queryset=nomina)
        nomina = myFilter.qs
    else:
        return redirect('home_reportes')
    return render(request, 'reportes/resultado.html', {'tipo_reporte': tipo_reporte, 'modules': modules, 'url_name': 'reportes', 'resultados':resultados,'myFilter':myFilter})


"""Inicio de vistas prepocesamiento"""
@login_required(login_url='login')
@allowed_users(['preprocesamiento'])
def preprocesamiento_home(request):
    estados_bloqueantes = ['subidos_archivos',
                            'cargando_db',
                            'generando_liquidaciones'
                           ]

    context = {}
    periodo_actual = datetime.datetime.now().strftime('%Y-%m')
    preprocesamiento_actual = Preprocesamiento.objects.filter(periodo_id=int(periodo_actual.replace('-', '')), empresa_id= request.session['id_empresa'])
    if len(preprocesamiento_actual)>0:
        preprocesamiento_actual = preprocesamiento_actual[0]
        if preprocesamiento_actual.estado in estados_bloqueantes:
            messages.warning(request, 'Actualmente se esta trabajando en el preprocesamiento del periodo {}'.format(periodo_actual))
            context.update({'habilitar_carga': False})
        elif preprocesamiento_actual.estado=='liquidacion_disponible':
            messages.success(request, 'El procesamiento para el periodo actual ha finalizado, por favor dirigase a la seccion de liquidaciones para descargar el resultado final')
            context.update({'habilitar_carga': False})
        elif preprocesamiento_actual.estado == 'error_mi_planilla':
            messages.error(request, 'El resultado del periodo actual no ha sido aprobado por mi planilla, vuelva a crear un preprocesamsiento porfavor')
            context.update({'habilitar_carga':True})
        elif preprocesamiento_actual.estado == 'exito_mi_planilla':
            messages.success(request, 'Las liquidaciones se encuentran al dia')
            context.update({'habilitar_carga': False})
    else:
        messages.success(request, 'Por favor cargue los archivos para preprocesar el periodo actual')
        context.update({'habilitar_carga': True})
    context.update({'periodo_actual': periodo_actual})
    preprocesamientos_pendientes = Preprocesamiento.objects.filter(Q(estado='cargando_db') | Q(estado='subidos_archivos') | Q(estado='generando_liquidaciones'))
    preprocesamientos = Preprocesamiento.objects.filter(empresa_id=request.session['id_empresa'])
    context.update({'modules': get_modules(request), 'url_name': 'preprocesamiento'})
    if(block_load_file(preprocesamientos_pendientes)):
        messages.warning(request, 'El servidor dedicado se encuentra trabajando, la carga de preprocesamientos esta deshabilitada')
        context.update({'habilitar_carga': False})
    else:
        messages.info(request, 'El servidor dedicado esta disponible para procesar')
    context.update({'preprocesamientos': preprocesamientos})
    return render(request, 'preprocesamiento/preprocesamiento_home.html', context)


@login_required(login_url='login')
@allowed_users(['preprocesamiento'])
def preprocesamiento_crear(request):
    #TODO obtener preprocesamientos y validar resultados para permitir cargar archivos o no
    periodo_actual = datetime.datetime.now().strftime('%Y%m')
    periodo_modelo = Periodo.objects.filter(id_periodo=periodo_actual)
    modules = get_modules(request)
    return render(request, 'preprocesamiento/preprocesamiento_result.html', {'url_name':'preprocesamiento', 'modules':modules})


@login_required(login_url='login')
@allowed_users(['preprocesamiento'])
def preprocesamiento_descargar(request, file_type, file_name):
    #TODO: Validar el nombre del archivo para que no pueda ser descargado nada fuera de la empresa
    if file_type=='planta':
        preprocesamiento = Preprocesamiento.objects.filter(planta='path/'+file_name, empresa=request.session['id_empresa'])
    elif file_type=='nomina':
        preprocesamiento = Preprocesamiento.objects.filter(nomina='path/'+file_name, empresa=request.session['id_empresa'])
    elif file_type=='novedades':
        preprocesamiento = Preprocesamiento.objects.filter(novedades='path/'+file_name, empresa=request.session['id_empresa'])
    else:
        messages.error(request, 'Tipo de archivo invalido')
        return redirect('inicio')
    print(file_name)
    if len(preprocesamiento)>0:
        print('encontrado')
        file = open('media/path/'+file_name, 'rb')
        return FileResponse(file, as_attachment=True)
    else:
        print('No encontrado')
        messages.error(request, 'No esta en la empresa correcta o el archivo no existe')
        return redirect('inicio')
    modules = get_modules(request)
    return render(request, 'preprocesamiento/preprocesamiento_result.html', {'url_name':'preprocesamiento', 'modules':modules})


"""Fin de vistas de preprocesamiento"""

@login_required(login_url='login')
@allowed_users(['liquidaciones'])
def liquidaciones_home(request):
    modules = get_modules(request)
    return render(request, 'liquidaciones/liquidaciones_home.html', {'modules': modules, 'url_name': 'liquidaciones'})


"""Inicio de vistas de parametros"""
@login_required(login_url='login')
@allowed_users(['parametros'])
def parametros_home(request):
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
    print(formulario)
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
    log = Log.objects.filter(empresa_id = request.session['id_empresa'])
    modules = get_modules(request)
    myFilter = LogsFilter(request.GET, queryset=log)
    log = myFilter.qs
    return render(request, 'logs/logs_home.html', {'modules': modules, 'url_name': 'logs', 'logs':log, 'myFilter':myFilter})


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