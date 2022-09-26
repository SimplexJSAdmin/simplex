import datetime, requests, os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry



def login__():
    client = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    client.mount('http://', adapter)
    client.mount('https://', adapter)
    response_1 = client.get(os.environ.get('DOMAIN_BACK_1')+'/app/login',  timeout=11)
    print('Response1:',"-"*15,response_1)
    csrf_token = client.cookies['csrftoken']
    login_data = {'username':'root', 'pass':'root', 'csrfmiddlewaretoken':csrf_token}
    r1 = client.post(os.environ.get('DOMAIN_BACK_1')+'/app/login', data=login_data,  timeout=10)
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


# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from calendar import monthrange
from zoneinfo import ZoneInfo # noqa
import math

from os.path import exists
import pandas as pd
import re

from .exceptions import *
from .constant import *


# -------------------------------------------------------------------
def round_100(x: float, multiple: int = 100) -> float:
    """
    Genera aproximación a un multiplo

    Args:
        x (float):
            Número a aproximar
        multiple (int):
            Multiplo a utilzar

    Return:
        Número aproximado
    """
    return math.ceil(float(x) / multiple) * multiple


# -------------------------------------------------------------------
def sumar(*args):
    """
    Realiza la suma de los valores

    Args:
        *args:
            Lista de argumentos a sumar
    """
    value = 0

    for i in args:
        if not isinstance(i, (int, float)):
            i = 0

        value += i

    return value


# -------------------------------------------------------------------
def leer_datos_archivo(path: str) -> pd.DataFrame:
    """
    Carga en memoria los datos de un archivo

    Args:
        path (str):
            Ruta del archivo

    Return:
        True si el texto coincide con el patrón, False en caso
        contrario
    """
    if not isinstance(path, str):
        raise InvalidParameterFunctions('path', 'String')

    if exists(path):
        if re.match(r'.+\.csv$', path):
            data = pd.read_csv(path, dtype='string')

        elif re.match(r'.+\.xlsx*$', path):
            data = pd.read_excel(path)

        else:
            print('Tipo de archivo no disponible')
            data = pd.DataFrame()

    else:
        raise FileNotExists(path)

    return data


# -------------------------------------------------------------------
def comparar_patron(text: str, pattern: str) -> bool:
    """
    Verifica que un texto cumpla con un patrón determinado

    Args:
        text (str):
            Texto que se desea verificar
        pattern (str):
            Patrón de comparación

    Return:
        True si el texto coincide con el patrón, False en caso
        contrario
    """
    if not isinstance(text, str):
        raise InvalidParameterFunctions('text', 'String')

    if re.match(pattern, text):
        return True
    else:
        return False


# -------------------------------------------------------------------
def generar_fechas(year: str = None,
                   month: str = None,
                   delta_month: int = None,
                   string: bool = True,
                   format: str = '%Y-%m-%d') -> tuple:
    """
    Genera una tupla con las fechas del primer y último día de un mes

    Args:
        year (str):
            Año
        month (str):
            Mes
        delta_month (int):
            Meses hacia atrás que se requiere generar la fecha
        string (bool):
            Define la salida de la función, si es True
            retorna un string, en caso contrario un objeto datetime
        format (str):
            Formato de salida del string, aplica si string es True

    Return:
        Tupla con los string de las fechas
    """
    if not isinstance(year, (str, int)):
        year_tmp = datetime.now(ZoneInfo('America/Bogota')) - timedelta(days=30)
        year = year_tmp.year

    if not isinstance(month, (str, int)):
        month_tmp = datetime.now(ZoneInfo('America/Bogota')) - timedelta(days=30)
        month = month_tmp.month

    year = str(year)
    month = str(month)

    if year.isdigit() and month.isdigit():
        date_aux = datetime(int(year), int(month), 1)

        if isinstance(delta_month, int):
            if delta_month > 0:
                month_estimate = delta_month * 30
                date_aux = date_aux - timedelta(days=month_estimate)

        day_n = monthrange(date_aux.year, date_aux.month)[1]

        date_1 = datetime(date_aux.year, date_aux.month, 1)
        date_2 = datetime(date_aux.year, date_aux.month, day_n)

        if string:
            return date_1.strftime(format), date_2.strftime(format)
        else:
            return date_1, date_2


# -------------------------------------------------------------------
def generar_linea_txt(*args) -> str:
    """
    Genera la línea del TXT para un empleado en particular

    Args:
        *args:
            Lista de valores asociados al empleado, esta lista
            debe estar en el mismo orden del TXT
    Return:
        Línea del TXT
    """
    if len(args) != 97:
        raise NumberFieldIncorrect()

    code_txt = ''

    for valor, tipo, longitud in zip(args, FIELDS_TYPE, FIELDS_LEN):
        code_txt += generar_cod(valor, tipo, longitud)

    return code_txt


# -------------------------------------------------------------------
def generar_cod(campo: str, clasif: str, longitud: int) -> str:
        """
        Estandariza y genera el código de acuerdo a la clasificación
        del campo y la longitud requerida

        Args:
            campo (str):
                Texto o número del usuario que se va a estandarizar
            clasif (str):
                Clasificación del campo: N (númerico) o
                A (alfanumérico o texto)
            longitud (int):
                Longitud requerida del campo

        Return:
            Campo codificado de acuerdo al requerimiento
        """
        if not isinstance(clasif, str):
            raise InvalidParameterFunctions('clasif',
                                            'string o entero')

        if not isinstance(longitud, int) or longitud < 1:
            raise InvalidParameterFunctions('longitud',
                                            'entero',
                                            'mayor a cero')

        if campo is None:
            campo = ''

        if re.match('^n.*', clasif, flags=re.IGNORECASE):
            return '{:.0f}'.format(round(campo, 0)).zfill(longitud)

        elif re.match('^t.*', clasif, flags=re.IGNORECASE) \
            or re.match('^a.*', clasif, flags=re.IGNORECASE):
            return str(campo).upper().ljust(longitud)

        elif re.match('^p.*', clasif, flags=re.IGNORECASE):
            if not isinstance(campo, float):
                campo = 0.0

            return '{}'.format(round(campo, 5)).ljust(longitud, '0')

        else:
            raise InvalidOptionFunctions('clasif', 'texto',
                                         'alfanumérico', 'número',
                                         'porcentaje')


def decodificar_txt(line: str, clear: bool = False) -> namedtuple:
    """
    Permite analizar un txt y retornar los campos separados

    Args:
        line (str):
            Línea del txt a decodificar
        clear (bool):
            El parámetro permite indicar si se realiza una limpieza
            sobre los datos de la tupla, por defecto False

    Return:
        Tupla con los campos
    """
    if not isinstance(line, str):
        raise InvalidParameterFunctions('line', 'string')

    decode_field = []
    begin = 0
    end = 0

    for f in FIELDS_LEN:
        end += f
        field_tmp = line[begin:end]

        if clear:
            tmp = re.sub(r'(^\s*|\s*$)', '', field_tmp)
            tmp = re.sub(r'^0+\.', '0.', tmp)

            decode_field.append(tmp)
        else:
            decode_field.append(field_tmp)

        begin = end

    return decode_field

