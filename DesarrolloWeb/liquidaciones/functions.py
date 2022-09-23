import datetime


def get_modules(request):
    if request.user.is_authenticated:
        modules_names = [*map(lambda x: x.name, request.user.groups.all())]
        return modules_names
    else:
        return []


def block_load_file(preprocesos):
    if len(preprocesos) > 0:
        return True
    return False


def validar_preprocesamiento_actual(request, preprocesamiento_actual, context, messages):
    periodo_actual = get_periodo_actual()['cod']
    estados_bloqueantes = ['subidos_archivos',
                           'cargando_db',
                           'generando_liquidaciones'
                           ]
    if len(preprocesamiento_actual) > 0:
        preprocesamiento_actual = preprocesamiento_actual[0]
        if preprocesamiento_actual.estado in estados_bloqueantes:
            context.update({'habilitar_carga': False, 'swal_alert': {
                'message': 'Actualmente se esta trabajando en el preprocesamiento del periodo {}'.format(
                    periodo_actual), 'icon_name': 'warning'}})
            return False
        elif preprocesamiento_actual.estado == 'liquidacion_disponible':
            messages.success(request,
                             'El procesamiento para el periodo actual ha finalizado, por favor dirigase a la seccion de liquidaciones para descargar el resultado final')
            context.update({'habilitar_carga': False})
            return False
        elif preprocesamiento_actual.estado == 'error_mi_planilla':
            messages.error(request,
                           'El resultado del periodo actual no ha sido aprobado por mi planilla, vuelva a crear un preprocesamsiento porfavor')
            context.update({'habilitar_carga': True})
            return True
        elif preprocesamiento_actual.estado == 'exito_mi_planilla':
            messages.success(request, 'Las liquidaciones se encuentran al dia')
            context.update({'habilitar_carga': False})
            return False
    else:
        context.update({'habilitar_carga': True, 'swal_alert': {
            'message': 'Para el periodo actual no se han creado preprocesamientos', 'icon_name': 'success'}})
        return True


def get_periodo_actual():
    def validar_mes(mes):
        mes = str(mes)
        return '0' + mes if len(mes) == 1 else mes

    hoy = datetime.datetime.now()
    if hoy.month == 1:
        return {'year': str(hoy.year - 1), 'month': '12', 'cod': str(hoy.year - 1) + str(hoy.month)}
    else:
        return {'year': str(hoy.year), 'month': validar_mes(hoy.month - 1),
                'cod': str(hoy.year) + validar_mes(hoy.month - 1)}
