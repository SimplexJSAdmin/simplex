import re, os
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from .models import Empresa, EmpresasPermitidas, Planta, ParametrosEPS, ParametrosFSP, ParametrosAFP, ParametrosARL, \
    ParametrosCAJA, ParametrosICBF, ParametrosSENA, ConceptoEmpresa, ConceptoInterno, Log
from .forms import *
from .decorators import *
from .functions import *
from .filters import LogsFilter, ReporteNomina, ReporteLiquidaciones, ReportePlanta


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
    empresas_permitidas = EmpresasPermitidas.objects.filter(id_usuario=request.user.id)
    print(empresas_permitidas)
    modules = get_modules(request)
    return render(request, "index.html",
                  {'modules': modules, 'url_name': 'inicio', 'empresas_permitidas': empresas_permitidas})


@login_required(login_url='login')
@allowed_users(['reportes'])
def obtener_reportes_opciones(request, empresa_sesion):
    try:
        del (request.session['tipo_reporte'])
    except:
        print('no se habia creado tipo de reporte')
    modules = get_modules(request)
    opciones_reporte = {'nomina': 'Nómina', 'planta': 'Planta', 'liquidaciones': 'Liquidaciones', 'medios_magneticos':'MediosMagneticos'}
    return render(request, 'reportes/obtener_reportes.html',
                  {'opciones': opciones_reporte, 'modules': modules, 'url_name': 'reportes',
                   'empresa_seleccionada': empresa_sesion})


@login_required(login_url='login')
@allowed_users(['reportes'])
def obtener_reportes_final(request, empresa_sesion):
    modules = get_modules(request)
    context = {}
    if 'tipo_reporte' in request.session.keys():
        tipo_reporte = request.session['tipo_reporte']
        context.update({'tipo_reporte': tipo_reporte})
        if tipo_reporte == 'nomina':
            print('nomina')
            resultados = Nomina.objects.filter(empresa_id=request.session['id_empresa'])
            myFilter = ReporteNomina(request.POST, queryset=resultados)
            resultados = myFilter.qs
        elif tipo_reporte == 'planta':
            resultados = Planta.objects.filter(id_empresa=request.session['id_empresa'])
            myFilter = ReportePlanta(request.POST, queryset=resultados)
            resultados = myFilter.qs
        elif tipo_reporte == 'liquidaciones':
            resultados = Liquidaciones.objects.filter(id_empresa=request.session['id_empresa'])
            myFilter = ReporteLiquidaciones(request.POST, queryset=resultados)
            resultados = myFilter.qs
        else:
            messages.error(request, 'Url invalida')
            return redirect('inicio')
        context.update({'resultados': resultados, 'myFilter': myFilter})
    else:
        print('creando dato en la sesion')
        request.session['tipo_reporte'] = request.POST['tipo_reporte']
        return redirect('reportes_result')
    context.update({'modules': modules, 'url_name': 'reportes', 'empresa_seleccionada': empresa_sesion})
    return render(request, 'reportes/reportes_resultado.html', context)




"""Inicio de vistas prepocesamiento"""

@login_required(login_url='login')
@allowed_users(['preprocesamiento'])
def preprocesamiento_home(request, empresa_sesion):
    context = {}
    context.update({'empresa_seleccionada': empresa_sesion})
    periodo_actual = get_periodo_actual()
    context.update({'periodo_actual': periodo_actual})
    preprocesamiento_actual = Preprocesamiento.objects.filter(periodo_id=periodo_actual['cod'],
                                                              empresa_id=request.session['id_empresa'])
    validar_preprocesamiento_actual(request, preprocesamiento_actual, context, messages)
    preprocesamientos_pendientes = Preprocesamiento.objects.filter(
        Q(estado='cargando_db') | Q(estado='subidos_archivos') | Q(estado='generando_liquidaciones'))
    preprocesamientos = Preprocesamiento.objects.filter(empresa_id=request.session['id_empresa'])
    context.update({'modules': get_modules(request), 'url_name': 'preprocesamiento'})
    if (block_load_file(preprocesamientos_pendientes)):
        messages.warning(request,
                         'El servidor dedicado se encuentra trabajando, la carga de preprocesamientos esta deshabilitada')
        context.update({'habilitar_carga': False})
    else:
        messages.info(request, 'El servidor dedicado esta disponible para procesar')
    context.update({'preprocesamientos': preprocesamientos})
    return render(request, 'preprocesamiento/preprocesamiento_home.html', context)


@login_required(login_url='login')
@allowed_users(['preprocesamiento'])
def cargar_preprocesamiento(request, empresa_sesion):
    """INICIO DE PROCESADO EN EL BACK 2"""
    # TODO: Poner esta ruta como variable de entorno
    cliente = requests.session()
    periodo_actual = get_periodo_actual()
    url_back_2 = 'http://127.0.0.1:8001/cargar-registros-bd/'
    preprocesamiento_creado = Preprocesamiento.objects.filter(periodo_id=periodo_actual['cod'],
                                                              empresa_id=request.session['id_empresa'])[0]
    url = url_back_2+str(preprocesamiento_creado.periodo_id)+'/'+str(preprocesamiento_creado.empresa_id)
    print(url)
    response = cliente.get(url, verify=False)
    print(response)
    return redirect('preprocesamiento')


@login_required(login_url='login')
@allowed_users(['preprocesamiento'])
def preprocesamiento_crear(request, empresa_sesion):
    # TODO obtener preprocesamientos y validar resultados para permitir cargar archivos o no
    modules = get_modules(request)
    context = {'url_name': 'preprocesamiento', 'modules': modules, 'empresa_seleccionada': empresa_sesion}
    periodo_actual = get_periodo_actual()

    if request.method == 'POST':
        preprocesamiento_actual = Preprocesamiento.objects.filter(periodo_id=periodo_actual['cod'],
                                                                  empresa_id=request.session['id_empresa'])
        preprocesamiento_actual_validado = validar_preprocesamiento_actual(request, preprocesamiento_actual, context, messages)
        if preprocesamiento_actual_validado['accion']== 'crear':
            periodo = Periodo.objects.filter(id_periodo=periodo_actual['cod'])
            if len(periodo) == 0:
                periodo_nuevo = Periodo(id_periodo=periodo_actual['cod'], mes_periodo=periodo_actual['month'],
                                        year_periodo=periodo_actual['year'])
                periodo_nuevo.save()
            else:
                preprocesamiento = Preprocesamiento()
                preprocesamiento.user = request.user
                preprocesamiento.empresa = Empresa.objects.get(id_empresa=request.session['id_empresa'])
                preprocesamiento.planta = request.FILES['planta']
                preprocesamiento.nomina = request.FILES['nomina']
                preprocesamiento.novedades = request.FILES['novedades']
                preprocesamiento.periodo = Periodo.objects.get(id_periodo=periodo_actual['cod'])
                preprocesamiento.estado = 'subidos_archivos'
                preprocesamiento.fecha = datetime.datetime.now()
                preprocesamiento.save()
                preprocesamiento_generado = Preprocesamiento.objects.filter(periodo_id=periodo_actual['cod'],
                                                                  empresa_id=request.session['id_empresa'])[0]
                url_back_2 = os.environ.get('DOMAIN_BACK_2')+':8001/home/'
                print(url_back_2)
                planta_file = open('media/'+str(preprocesamiento_generado.planta), 'rb')
                cliente = requests.Session()
                res_1 = cliente.get(url_back_2)
                print(res_1)
                csrf_token = cliente.cookies['csrftoken']
                response = requests.post(url_back_2, files={'planta': planta_file,  'csrfmiddlewaretoken':csrf_token})
                print(response)
                return redirect('preprocesamiento')
        else:
            preprocesamiento_actual[0].user = request.user
            preprocesamiento_actual[0].empresa = Empresa.objects.get(id_empresa=request.session['id_empresa'])
            preprocesamiento_actual[0].planta = request.FILES['planta']
            preprocesamiento_actual[0].nomina = request.FILES['nomina']
            preprocesamiento_actual[0].novedades = request.FILES['novedades']
            preprocesamiento_actual[0].periodo = Periodo.objects.get(id_periodo=periodo_actual['cod'])
            preprocesamiento_actual[0].estado = 'subidos_archivos'
            preprocesamiento_actual[0].fecha = datetime.datetime.now()
            preprocesamiento_actual[0].save()
            """INICIO DE PROCESADO EN EL BACK 2"""
            #TODO: Poner esta ruta como variable de entorno
            url_back_2 = 'http://localhost:8001/cargar-registros-bd/'
            planta_file = open(request.FILES['planta'], 'rb')
            response = requests.post(url_back_2, files={'planta':planta_file})
            return redirect('preprocesamiento')
    else:
        preprocesamientos_pendientes = Preprocesamiento.objects.filter(
            Q(estado='cargando_db') | Q(estado='subidos_archivos') | Q(estado='generando_liquidaciones'))
        if (block_load_file(preprocesamientos_pendientes)):
            return redirect('preprocesamiento')
        else:
            preprocesamiento_actual = Preprocesamiento.objects.filter(periodo_id=periodo_actual['cod'],
                                                                      empresa_id=request.session['id_empresa'])
            preprocesamiento_actual_validado = validar_preprocesamiento_actual(request, preprocesamiento_actual,
                                                                               context, messages)
            if not preprocesamiento_actual_validado:
                return redirect('preprocesamiento')
            else:
                form = FileForm(request.POST or None)
                if preprocesamiento_actual_validado['accion'] == 'crear':
                    context.update({'accion':'creando', 'form':form})
                    return render(request, 'preprocesamiento/preprocesamiento_result.html', context)

                else:
                    context.update({'accion': 'recargando', 'form': form})
                    return render(request, 'preprocesamiento/preprocesamiento_result.html', context)
            context.update({'form': form})
            return render(request, 'preprocesamiento/preprocesamiento_result.html', context)


@login_required(login_url='login')
@allowed_users(['preprocesamiento'])
def preprocesamiento_descargar(request, empresa_sesion, file_type, file_name):
    # TODO: Validar el nombre del archivo para que no pueda ser descargado nada fuera de la empresa
    if file_type == 'planta':
        preprocesamiento = Preprocesamiento.objects.filter(planta='path/' + file_name,
                                                           empresa=request.session['id_empresa'])
    elif file_type == 'nomina':
        preprocesamiento = Preprocesamiento.objects.filter(nomina='path/' + file_name,
                                                           empresa=request.session['id_empresa'])
    elif file_type == 'novedades':
        preprocesamiento = Preprocesamiento.objects.filter(novedades='path/' + file_name,
                                                           empresa=request.session['id_empresa'])
    else:
        messages.error(request, 'Tipo de archivo invalido')
        return redirect('inicio')
    print(file_name)
    if len(preprocesamiento) > 0:
        print('encontrado')
        file = open('media/path/' + file_name, 'rb')
        return FileResponse(file, as_attachment=True)
    else:
        print('No encontrado')
        messages.error(request, 'No esta en la empresa correcta o el archivo no existe')
        return redirect('inicio')
    modules = get_modules(request)
    return render(request, 'preprocesamiento/preprocesamiento_result.html',
                  {'url_name': 'preprocesamiento', 'modules': modules, 'empresa_seleccionada': empresa_sesion})


"""Fin de vistas de preprocesamiento"""


@login_required(login_url='login')
@allowed_users(['liquidaciones'])
def liquidaciones_home(request, empresa_sesion):
    modules = get_modules(request)
    return render(request, 'liquidaciones/liquidaciones_home.html',
                  {'modules': modules, 'url_name': 'liquidaciones', 'empresa_seleccionada': empresa_sesion})


"""Inicio de vistas de parametros"""


@login_required(login_url='login')
@allowed_users(['parametros'])
def parametros_home(request, empresa_sesion):
    modules = get_modules(request)
    return render(request, 'parametros/parametros_home.html',
                  {'modules': modules, 'url_name': 'parametros', 'empresa_seleccionada': empresa_sesion})


@login_required(login_url='login')
@allowed_users(['parametros'])
def parametros_list(request, empresa_sesion, parameter_type):
    modules = get_modules(request)
    context = {'modules': modules, 'url_name': 'parametros', 'parameter_type': parameter_type,
               'empresa_seleccionada': empresa_sesion}
    tablas_topes = {'eps': ParametrosEPS, 'afp': ParametrosAFP, 'fsp': ParametrosFSP, 'sena': ParametrosSENA,
                    'icbf': ParametrosICBF}
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
def conceptos_home(request, empresa_sesion):
    conceptos_empresa = ConceptoEmpresa.objects.filter(empresa_id=request.session['id_empresa'])
    # concepto_empresa = conceptos_empresa[0]
    # print(concepto_empresa.__dict__)
    modules = get_modules(request)
    return render(request, 'conceptos/conceptos_home.html',
                  {'modules': modules, 'url_name': 'conceptos', 'conceptos_empresa': conceptos_empresa,
                   'empresa_seleccionada': empresa_sesion})


@login_required(login_url='login')
@allowed_users(['conceptos'])
def conceptos_internos_home(request, empresa_sesion):
    modules = get_modules(request)
    conceptos_internos = ConceptoInterno.objects.all()
    return render(request, 'conceptos/internos/conceptos_internos_home.html',
                  {'url_name': 'conceptos', 'conceptos_internos': conceptos_internos, 'modules': modules,
                   'empresa_seleccionada': empresa_sesion})


@login_required(login_url='login')
@allowed_users(['conceptos'])
def conceptos_internos_crear(request, empresa_sesion):
    formulario = ConceptoInternoForm(request.POST or None)
    print(formulario)
    return render(request, 'conceptos/internos/conceptos_internos_crear.html',
                  {'formulario': formulario, 'empresa_seleccionada': empresa_sesion})


"""Fin de vistas de conceptos internos y de empresa"""


@login_required(login_url='login')
@allowed_users(['informes'])
def informes_home(request, empresa_sesion):
    modules = get_modules(request)
    return render(request, 'informes/informes_home.html',
                  {'modules': modules, 'url_name': 'informes', 'empresa_seleccionada': empresa_sesion})


@login_required(login_url='login')
@allowed_users(['logs'])
def logs_home(request, empresa_sesion):
    log = Log.objects.filter(empresa_id=request.session['id_empresa'])
    modules = get_modules(request)
    myFilter = LogsFilter(request.GET, queryset=log)
    log = myFilter.qs
    return render(request, 'logs/logs_home.html',
                  {'modules': modules, 'url_name': 'logs', 'logs': log, 'myFilter': myFilter,
                   'empresa_seleccionada': empresa_sesion})


"""
    Vistas relacionadas con el modulo empresa
"""


@login_required(login_url='login')
@allowed_users(['empresas'])
def empresas_home(request, empresa_sesion):
    empresas = Empresa.objects.all()
    modules = get_modules(request)
    return render(request, 'empresas/empresas_home.html',
                  {'modules': modules, 'url_name': 'empresas', 'empresas': empresas,
                   'empresa_seleccionada': empresa_sesion})


@login_required(login_url='login')
@allowed_users(['empresas'])
def empresas_crear(request, empresa_sesion):
    modules = get_modules(request)
    formulario = EmpresasCreateForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('empresas')
    return render(request, 'empresas/empresa_crear.html',
                  {'modules': modules, 'url_name': 'empresas', 'formulario': formulario,
                   'empresa_seleccionada': empresa_sesion})


"""
Fin modulo de empresas
"""


@login_required(login_url='login')
def logout(request):
    try:
        del (request.session['id_empresa'])
    except:
        pass
    if request.user.is_authenticated:
        logout_django(request)
    return redirect('login')
