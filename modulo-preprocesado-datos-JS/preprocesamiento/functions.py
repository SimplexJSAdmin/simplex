import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry



def login():
    client = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    client.mount('http://', adapter)
    client.mount('https://', adapter)

    #TODO definir como variables de entorno

    response_1 = client.get('http://172.21.0.4:8000/app/login',  timeout=11)
    print('Response1:',"-"*15,response_1)
    csrf_token = client.cookies['csrftoken']
    login_data = {'username':'root', 'pass':'root', 'csrfmiddlewaretoken':csrf_token}
    r1 = client.post('http://172.21.0.4:8000/app/login', data=login_data,  timeout=10)
    return client

def logout(client):
    client.get('http://172.21.0.4:8000/app/logout')
    del(client)
    return True

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
                'message': 'El servidor se encuentra ocupado trabajando en el periodo: {}'.format(
                    periodo_actual), 'icon_name': 'warning'}})
            return False
        elif preprocesamiento_actual.estado == 'liquidacion_disponible':
            context.update({'habilitar_carga': False, 'swal_alert': {
                'message': 'El procesamiento para el periodo actual ha finalizado, por favor dirigase a la seccion de liquidaciones para descargar el resultado final', 'icon_name': 'success'}})
            return False
        elif preprocesamiento_actual.estado == 'error_mi_planilla':
            context.update({'habilitar_carga': True, 'swal_alert':{
                'message':'El resultado del periodo actual no ha sido aprobado por mi planilla, vuelva a crear un preprocesamsiento por favor',
                'icon_name': 'error'
            }})
            return {'resul':True, 'accion':'actualizar'}
        elif preprocesamiento_actual.estado == 'exito_mi_planilla':
            context.update({'habilitar_carga': False, 'swal_alert':{
                'message': 'Las liquidaciones se encuentran al dia',
                'icon_name': 'success'
            }})
            return False
    else:
        context.update({'habilitar_carga': True, 'swal_alert': {
            'message': 'Para el periodo actual no se han creado preprocesamientos, por favor cree uno',
            'icon_name': 'success'}})
        return {'resul':True, 'accion':'crear'}


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




def cargar_planta(planta):
    print(planta)

def cargar_nomina(nomina):
    print(nomina)

def cargar_novedades(novedades):
    print(novedades)

