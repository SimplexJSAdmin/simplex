import datetime

def get_modules(request):
    if request.user.is_authenticated:
        modules_names = [*map(lambda x: x.name, request.user.groups.all())]
        return modules_names
    else:
        return []

def block_load_file(preprocesos):
    if len(preprocesos)>0:
        return True
    return False

def validar_preprocesamiento_actual(request, preprocesamiento_actual, context, messages):
    periodo_actual = datetime.datetime.now().strftime('%Y-%m')
    estados_bloqueantes = ['subidos_archivos',
                           'cargando_db',
                           'generando_liquidaciones'
                           ]
    if len(preprocesamiento_actual)>0:
        preprocesamiento_actual = preprocesamiento_actual[0]
        if preprocesamiento_actual.estado in estados_bloqueantes:
            messages.warning(request, 'Actualmente se esta trabajando en el preprocesamiento del periodo {}'.format(periodo_actual))
            context.update({'habilitar_carga': False})
            return False
        elif preprocesamiento_actual.estado=='liquidacion_disponible':
            messages.success(request, 'El procesamiento para el periodo actual ha finalizado, por favor dirigase a la seccion de liquidaciones para descargar el resultado final')
            context.update({'habilitar_carga': False})
            return False
        elif preprocesamiento_actual.estado == 'error_mi_planilla':
            messages.error(request, 'El resultado del periodo actual no ha sido aprobado por mi planilla, vuelva a crear un preprocesamsiento porfavor')
            context.update({'habilitar_carga':True})
            return True
        elif preprocesamiento_actual.estado == 'exito_mi_planilla':
            messages.success(request, 'Las liquidaciones se encuentran al dia')
            context.update({'habilitar_carga': False})
            return False
    else:
        messages.success(request, 'Por favor cargue los archivos para preprocesar el periodo actual')
        context.update({'habilitar_carga': True})
        return True