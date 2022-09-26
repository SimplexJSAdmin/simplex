# -*- coding: utf-8 -*-
from collections import namedtuple
from .models import ParametrosGlobales, Empresa
from django.db.models import Q


global id_empresa
# from .models import Parametros


key_id = {
            'smmlv':1,
            'base_cotizacion':2,
            'salario_integral':3,
            'porcentaje':4
         }
SMMLV_VALOR = ParametrosGlobales.objects.filter(id=key_id['smmlv']).valor
NO_SMMLV_INTEGRAL = 10
PORCENTAJE_CARGA_PRESTACIONAL_INTEGRAL = 0.3

PORC_PAGOS_NO_SALARIALES = 0.4

COTIZACION_SALARIO_INTEGRAL = 0.7

EXONERACION_EMPRESA = Empresa.objects.filter(Q(id=5) | Q(descripcion='prueba')).descripcion

HORAS_POR_DIA = 8
INCLUIR_HORAS_DIA = False


# caja de compensación familiar
PORC_CCF = 0.04


# parafiscales
PORC_SENA = 0.02
PORC_ICBF = 0.03


# fondo de solidaridad (FSP)
TOPE_MINIMO_FONDO_SOLIDARIDAD_SMMLV = 4 * SMMLV_VALOR
PORC_FSP = 0.005


# fondo de subsistencia (FS)
TOPE_MINIMO_FONDO_SUBSISTENCIA_SMMLV = 4 * SMMLV_VALOR
PORC_FS = 0.005

TOPE_2_FONDO_SUBSISTENCIA_SMMLV = 16 * SMMLV_VALOR
PORC_TOPE_2 = PORC_FS + 0.002

TOPE_3_FONDO_SUBSISTENCIA_SMMLV = 17 * SMMLV_VALOR
PORC_TOPE_3 = PORC_FS + 0.004

TOPE_4_FONDO_SUBSISTENCIA_SMMLV = 18 * SMMLV_VALOR
PORC_TOPE_4 = PORC_FS + 0.006

TOPE_5_FONDO_SUBSISTENCIA_SMMLV = 19 * SMMLV_VALOR
PORC_TOPE_5 = PORC_FS + 0.008

TOPE_6_FONDO_SUBSISTENCIA_SMMLV = 20 * SMMLV_VALOR
PORC_TOPE_6 = PORC_FS + 0.01


# salud
TOPE_MAX_SALUD = 25
TOPE_MIN_SALUD = 1

PORC_SALUD_EMPLEADO_BAS = 0.04
PORC_SALUD_EMPLEADO_INT = 0.125

TOPE_CAMBIO_PERC_SALUD = 10 * SMMLV_VALOR


# pension
TOPE_MAX_PENSION = 25
TOPE_MIN_PENSION = 1

PORC_PENSION_TOTAL = 0.16
PORC_PENSION_EMPLEADO = 0.04
PORC_PENSION_EMPLEADOR = 0.12


# arl
TOPE_MAX_RIESGOS = 25
TOPE_MIN_RIESGOS = 1

PORC_ARL_I = 0.00522
PORC_ARL_II = 0.01044
PORC_ARL_III = 0.02436
PORC_ARL_IV = 0.04350
PORC_ARL_V = 0.06960

Empleado = namedtuple(
    'Empleado',
    [
        'Tipo_de_registro', 'Secuencia',
        'Tipo_documento_cotizante', 'No_de_documento_cotizante',
        'Tipo_de_cotizante', 'Subtipo_de_cotizante',
        'Extranjero', 'Colombiano_en_el_exterior',
        'Cod_departamento', 'Cod_ciudad',
        'Primer_apellido', 'Segundo_apellido',
        'Primer_nombre', 'Segundo_nombre',
        'Ingreso', 'Retiro',
        'Traslado_desde_EPS', 'Traslado_hacia_EPS',
        'Traslado_desde_pension', 'Traslado_hacia_pension',
        'Variacion_permanente_salario', 'Correccion',
        'Variacion_transitoria_salario', 'Suspension_temporal',
        'Incapacidad_temporal', 'Licencia_maternidad_paternidad',
        'Vacaciones_licencia_remunerada', 'Aporte_voluntario',
        'Variacion_centro_de_trabajo', 'Dias_incapacidad',
        'Cod_fondo_pension_actual', 'Cod_fondo_pension_traslado',
        'Cod_EPS_actual', 'Cod_EPS_traslado',
        'Cod_CCF_actual', 'Dias_pension',
        'Dias_salud', 'Dias_ARL', 'Dias_CCF',
        'Salario_basico', 'Tipo_de_salario',
        'IBS_pension', 'IBC_salud', 'IBC_ARL', 'IBC_CCF',
        'Tarifa_pensiones', 'Cotizacion_obligatoria_pensiones',
        'Aporte_voluntario_afiliado_pensiones', 'Aporte_voluntario_aportante_pensiones',
        'Total_cotizacion_pensiones', 'Aporte_solidaridad_solidaridad',
        'Aporte_solidaridad_subsistencia', 'Valor_no_retenido',
        'Tarifa_salud', 'Cotizacion_obligatoria_salud',
        'UPC_ADRES', 'Autorizacion_incapacidad',
        'Valor_incapacidad', 'Autorizacion_licencia',
        'Valor_licencia', 'Tarifa_ARL',
        'Centro_de_trabajo', 'Cotizacion_obligatoria_ARL',
        'Tarifa_CCF', 'Valor_aporte_CCF',
        'Tarifa_SENA', 'Valor_aporte_SENA',
        'Tarifa_ICBF', 'Valor_aporte_ICBF',
        'Tarifa_ESAP', 'Valor_aporte_ESAP',
        'Tarifa_MEN', 'Valor_aporte_MEN',
        'Tipo_documento_cotizante_principal', 'No_documento_cotizante_principal',
        'Exonerado_de_pago_salud_SENA_ICBF', 'Cod_ARL_actual',
        'Clase_riesgo_afiliado', 'Indicador_tarifa_especial_pensiones',
        'Fecha_de_ingreso', 'Fecha_retiro',
        'Fecha_inicio_VSP', 'Fecha_inicio_SLN',
        'Fecha_fin_SLN', 'Fecha_inicio_IGE',
        'Fecha_fin_IGE', 'Fecha_inicio_LMA',
        'Fecha_fin_LMS', 'Fecha_inicio_VAC_LR',
        'Fecha_fin_VAC_LR', 'Fecha_inicio_VCT',
        'Fecha_fin_VCT', 'Fecha_inicio_IRL',
        'Fecha_fin_IRL', 'IBC_otros_parafiscales',
        'Número_de_horas_laboradas', 'Fecha_radicion_en_el_exterior'
    ],
    defaults = (None, ) * 97
)

FIELDS_LEN = (
    2, 5, 2, 16, 2, 2, 1, 1, 2, 3, 20, 30, 20, 30, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 6, 6, 6, 6, 6, 2, 2, 2, 2, 9, 1, 9,
    9, 9, 9, 7, 9, 9, 9, 9, 9, 9, 9, 7, 9, 9, 15, 9, 15, 9, 9, 9, 9,
    7, 9, 7, 9, 7, 9, 7, 9, 7, 9, 2, 16, 1, 6, 1, 1, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 3, 10
)

FIELDS_TYPE = (
    'Numérico', 'Numérico', 'Texto', 'Alfanumérico',
    'Numérico', 'Numérico', 'Texto', 'Texto', 'Numérico',
    'Numérico', 'Texto', 'Texto', 'Texto', 'Texto', 'Alfanumérico',
    'Alfanumérico', 'Alfanumérico', 'Alfanumérico', 'Alfanumérico',
    'Alfanumérico', 'Texto', 'Texto', 'Texto', 'Texto', 'Texto',
    'Texto', 'Texto', 'Texto', 'Texto', 'Numérico', 'Alfanumérico',
    'Alfanumérico', 'Alfanumérico', 'Alfanumérico', 'Alfanumérico',
    'Numérico', 'Numérico', 'Numérico', 'Numérico', 'Numérico',
    'Texto', 'Numérico', 'Numérico', 'Numérico', 'Numérico',
    'Porcentaje', 'Numérico', 'Numérico', 'Numérico', 'Numérico',
    'Numérico', 'Numérico', 'Numérico', 'Porcentaje', 'Numérico',
    'Numérico', 'Alfanumérico', 'Numérico', 'Alfanumérico',
    'Numérico', 'Porcentaje', 'Numérico', 'Numérico', 'Porcentaje',
    'Numérico', 'Porcentaje', 'Numérico', 'Porcentaje', 'Numérico',
    'Porcentaje', 'Numérico', 'Porcentaje', 'Numérico', 'Texto',
    'Alfanumérico', 'Texto', 'Alfanumérico', 'Numérico', 'Texto',
    'Texto', 'Texto', 'Texto', 'Texto', 'Texto', 'Texto', 'Texto',
    'Texto', 'Texto', 'Texto', 'Texto', 'Texto', 'Texto', 'Texto',
    'Texto', 'Numérico', 'Numérico', 'Texto'
)

# columnas requeridas por archivo
COLS_NOMINA_ACTUAL = [
    'no_personal', 'cod_concepto', 'desc_concepto', 'cantidad',
    'importe'
]

COLS_NOMINA_ANTERIOR = [
    'no_personal', 'cod_concepto', 'desc_concepto', 'cantidad', 'importe'
]

COLS_PLANTA_ACTUAL = [
    'no_personal', 'tipo_documento', 'clase_contrato','documento',
    'primer_apellido', 'segundo_apellido', 'primer_nombre',
    'segundo_nombre', 'importe', 'fecha', 'desde',
    'grupo_personal', 'clase'
]

COLS_PLANTA_ANTERIOR = [
    'no_personal', 'tipo_documento', 'documento', 'primer_apellido',
    'segundo_apellido', 'primer_nombre', 'segundo_nombre',
    'importe', 'fecha', 'desde', 'grupo_personal', 'clase'
]

COLS_LIQUIDACION_ACTUAL = None

COLS_LIQUIDACION_ANTERIOR = [
    'num_doc_cotizante', 'aporte_voluntario',
    'cod_fondo_pension_pertence', 'cod_eps_pertenece',
    'cod_ccf_pertenece', 'tipo_salario',
    'aporte_voluntario_afiliado_pension',
    'aporte_voluntario_aportante_pension',
    'valor_no_retenido', 'ups_adres',
    'centro_trabajo', 'tarifa_esap', 'tarifa_men',
    'exonerado_pago_eps_sena_icbf',
    'cod_arl_pertenece', 'clase_riesgo_afiliado',
    'indicador_tarifa_especial_pension',
    'fecha_inicio_vsp', 'fecha_inicio_sln',
    'fecha_fin_sln', 'fecha_inicio_ige', 'fecha_fin_ige',
    'fecha_inicio_lma', 'fecha_fin_lma', 'fecha_inicio_vac',
    'fecha_fin_vac', 'fecha_inicio_vct', 'fecha_inicio_vct',
    'fecha_inicio_irl', 'fecha_fin_irl', 'fecha_radicacion_exterior'
]

# casos especiales
CASO_ESPECIAL = [
    'Vacaciones Disfrutadas', 'Aporte Voluntario',
    'Incap.General Ambulatoria', 'Pago Vacaciones en Dinero',
    'Vacaciones Comp. en Term.', 'Licencia no remunerada',
    'Licencia Maternidad', 'Prórroga Incap Gral Ambul',
    'Licencia con Goce', 'Licencia Paternidad', 'Auxilio incapacidad',
    'Ajuste Salario Integral', 'Incap.Enfermedad Profesio'
]

INFO_CONCEPTOS = {
    'cod_concepto':
        ['2170', '2171', '2180', '2247', '2248', '3082', '3083', '3700', '7000', '7001', '7700', '9100', '9101', '9110', '9398', '9493', '9730', '9731', '1ABP', '1ASI', '1BAC', '1BAD', '1BAE', '1BAF', '1BAG', '1BAH', '1BAJ', '1BAM', '1BAP', '1BAT', '1BAV', '1BCC', '1BEX', '1BGL', '1BHC', '1BHD', '1BML', '1BNS', '1BPC', '1BPE', '1BPR', '1BPS', '1BPT', '1BPU', '1BPV', '1BPW', '1BPX', '1BRE', '1BRF', '1BRN', '1BVA', '1BVD', '1BVP', '1BVS', '1GRE', '1GUP', '1M50', '1M90', '1M95', '1M96', '1MAC', '1MCH', '1MGU', '1MGV', '1MPR', '1MST', '1NBM', '1NBP', '1RET', '1SDV', '1VAL', '2ACU', '2AIN', '2ANP', '2ANT', '2ART', '2DAP', '2DAU', '2DCE', '2DES', '2DPS', '2DVI', '2EMI', '2LCF', '2LCO', '2RSU', '2SDV', '2T04', '2T05', '2T13', '2T14', '2T17', '2T18', '2T26', '2T28', '2T30', '2T31', '2T32', '2T33', '2T34', '2T37', '2T38', '2T54', '2VAI', '3PBB', '3PBC', '3PCF', '3PCI', '3PCL', '3PCO', '3PDA', '3PEM', '939A', '97A1', '97D0', '9ANP', '9ANT', '9BGC', '9BGD', '9M40', '9R34', '9T26', 'BN02', 'BN03', 'BN04', 'M010', 'M020', 'M050', 'M100', 'M105', 'M110', 'M120', 'M130', 'M140', 'M150', 'M155', 'M1A1', 'M1A2', 'M1A3', 'M1A4', 'M1L1', 'M1L2', 'M1L3', 'M200', 'M350', 'M398', 'M399', 'M400', 'M401', 'M403', 'M421', 'M422', 'M423', 'M424', 'M425', 'M426', 'M427', 'M428', 'M429', 'M460', 'M480', 'T000', 'T001', 'T010', 'T011', 'T020', 'T030', 'T032', 'T050', 'T053', 'T056', 'T059', '/365', '/375', '/376', '/385', '/390', '/391', '/392', '/407', '/417', '/437', '/447', '/559', '/561', '/563', '2BVA'],
    'nota':
        ['salarial', 'salarial', 'no salarial', 'salarial', 'salarial', 'no salarial', 'descuento', 'no salarial', 'descuento', 'descuento', 'descuento', 'no salarial', 'no salarial', 'no salarial', 'no aplica', 'no aplica', 'vacaciones', 'vacaciones', 'salarial', 'salarial', 'no salarial', 'descuento', 'no salarial', 'descuento', 'no salarial', 'no salarial', 'no salarial', 'no salarial', 'no salarial', 'no salarial', 'no salarial', 'no salarial', 'no salarial', 'salarial', 'salarial', 'salarial', 'no salarial', 'no salarial', 'no salarial', 'salarial', 'salarial', 'no salarial', 'salarial', 'salarial', 'no salarial', 'salarial', 'salarial', 'no salarial', 'salarial', 'no salarial', 'no salarial', 'no salarial', 'no salarial', 'no salarial', 'no salarial', 'salarial', 'sostenimiento', 'salarial', 'salarial', 'salarial', 'no salarial', 'no salarial', 'salarial', 'salarial', 'no salarial', 'no salarial', 'salarial', 'salarial', 'salarial', 'no salarial', 'salarial', 'descuento', 'no salarial', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'vacaciones', 'vacaciones', 'descuento', 'no aplica', 'no aplica', 'no salarial', 'no salarial', 'vacaciones', 'descuento', 'descuento', 'no salarial', 'no salarial', 'no salarial', 'salarial', 'salarial', 'sostenimiento', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'salarial', 'no aplica', 'salarial', 'vacaciones', 'vacaciones', 'vacaciones', 'vacaciones', 'vacaciones', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'descuento', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica', 'no aplica'],
    'cuenta':
        ['54000086', '54000086', '54000051', '54000086', '54000086', '54000048', '54000048', 'Es un concepto Informativo, no se contabiliza, la contabilidad se realiza por la retencion que produce el pago', '22000042', '22000042', 'Es un concepto Informativo, no se contabiliza.', '54000051', '54000051', '57000034', '23000002', '23000002', '23000002', '54000000', '15400017', '54000000', '54000048', '54000048', '54000048', '54000048', '54000051', '54000051', '54000051', '54000051', '54000000', '54000068', '54000051', '54000051', '54000055', '54000031', '54000038', '54000034', '54000098', '54000009', '54000000', '23000025', '54000009', '54000000', '54000031', '54000031', '54000000', '54000086', '54000009', '54000055', '54000037', '57000013', '54000012', '54000000', '54000050', '54000000', '54000019', '54000000', '23000045', '54000000', '54000000', '54000000', '54000051', '54000051', '54000018', '54000031', '23000000', '54000000', '23000059', '23000047', '54000000', '54000017', '57000013', '206299', 'Es un concepto Informativo, no se contabiliza.', '206299', '206299', '206299', '23000065', '54000051', '22000016', '23000065', '215203', '206299', '23000045', '232176', '212065', '206299', '24000199', '207106', '207106', '54000066', '15400087', '54000066', '54000066', '206185', '225255', '229920', '23000045', '23000045', '54000066', '15400087', '54000066', '54000066', '206994', '24000202', '215202', '207107', '228803', '212064', '231424', '215201', '215198', '206299', '23000002', '54000000', '22000042', '206299', '206299', '54000020', '54000020', '23000002', '54000079', '206185', '54000017', '54000020', '54000020', '54000000', '54000000', '23000045', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '54000000', '23000002', '23000002', '23000002', '23000002', '23000002', '23000018', '23000019', '23000018', '23000019', '23000018', '23000019', '23000018', '23000019', '23000018', '23000000', '54000015', 'Se contabiliza al tercero que corresponda', 'Se contabiliza al tercero que corresponda', 'Se contabiliza al tercero que corresponda', 'Se contabiliza al tercero que corresponda', 'Se contabiliza al tercero que corresponda', 'Se contabiliza al tercero que corresponda', 'Se contabiliza al tercero que corresponda', '207106', '207106', '207106', '207106', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 'tipo': ['Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Descuento', 'Devengo ', 'Descuento', 'Descuento', 'Descuento', 'Devengo ', 'Devengo ', 'Devengo ', 'Informativo', 'Informativo', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Descuento', 'Devengo ', 'Descuento', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Descuento', 'Devengo ', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Devengo ', 'Devengo ', 'Descuento', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Descuento', 'Descuento', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Devengo ', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Descuento', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Informativo', 'Descuento']
}

CONCEPTOS_AUXILIOS = [
    '2180', '1BAG', '1BAH', '1BAJ', '1BAM', '1BAT', '1BAV', '1BPS', '1MAC', '1MST', 'M200'
    # sostenimientos '1M50', 'M050'
]

CONCEPTOS_INCAPACIDADES = [
    'M100', 'M105', 'M110', 'M140', 'M150', 'M1A1', 'M1A2', 'M1A3', 'M1A4'
]


# conceptos asociados a licencias
#CONCEPTOS_LICENCIAS = [
#    'M120', 'M130', 'M1L2', 'M1L3'
#]

CONCEPTOS_LICENCIAS = [*map(lambda x:str(x.codigo), ParametrosGlobales.object.filter(id_empresa= id_empresa).filter(tipo_novedad='lma'))]

CONCEPTOS_SLN = ['M1L2']


# conceptos asociados a vacaciones
CONCEPTOS_VACACIONES = [
    '9398', '9493', '9730', '9731', '939A', '97A1', 'M398', 'M399', 'M400', 'M401', 'M403', 'T001', 'T011', '/447'
]

CONCEPTOS_INGRESOS_EMPLEADOS = [
    'M020', 'M010', '1M50', 'M050'
]

NAME_COLS_TXT = [
    'tipo_registro', 'secuencia', 'tipo_doc_cotizante',
    'num_doc_cotizante', 'tipo_cotizante', 'subtipo_cotizante',
    'extranjero', 'colombian_en_exterior', 'cod_departamento',
    'cod_municipio', 'primer_apellido', 'segundo_apellido',
    'primer_nombre', 'segundo_nombre', 'ingreso', 'retiro',
    'traslado_desde_eps', 'traslado_hacia_eps',
    'traslado_desde_fondo_pension', 'traslado_hacia_fondo_pension',
    'variacion_permanente_salario', 'correcion',
    'variacion_transitoria_salario', 'suspencion_temporal',
    'incapacidad_temporal', 'licencia_maternidad_paternidad',
    'vacaciones_licencia_remunerada', 'aporte_voluntario',
    'variacion_centros_trabajo', 'dias_incapacidad',
    'cod_fondo_pension_pertence', 'cod_fondo_pension_tralasda',
    'cod_eps_pertenece', 'cod_eps_tralasda', 'cod_ccf_pertenece',
    'dias_fondo_pension', 'dias_eps', 'dias_arl', 'dias_ccf',
    'salario_basico', 'tipo_salario', 'ibc_fondo_pension', 'ibc_eps',
    'ibc_arl', 'ibc_ccf', 'tarifa_fondo_pension',
    'cotizacion_obligatoria_pension',
    'aporte_voluntario_afiliado_pension',
    'aporte_voluntario_aportante_pension', 'tota_cotizacion_pension',
    'aporte_fondo_solidaridad', 'aporte_fondo_subsistencia',
    'valor_no_retenido', 'tarifa_eps', 'cotizacion_obligatoria_eps',
    'ups_adres', 'autorizacion_incapacidad', 'valor_incapacidad',
    'autorizacion_licencia_maternidad', 'valor_licencia_maternidad',
    'tarifa_arl', 'centro_trabajo', 'cotizacion_obligatoria_arl',
    'tarifa_ccf', 'valor_aporte_ccf', 'tarifa_sena',
    'valor_aporte_sena', 'tarifa_icbf', 'valor_aporte_icbf',
    'tarifa_esap', 'valor_aporte_esap', 'tarifa_men',
    'valor_aporte_men', 'tipo_doc_cotizante_principal',
    'numero_doc_cotizante_principal', 'exonerado_pago_eps_sena_icbf',
    'cod_arl_pertenece', 'clase_riesgo_afiliado',
    'indicador_tarifa_especial_pension', 'fecha_ingreso',
    'fecha_retiro', 'fecha_inicio_vsp', 'fecha_inicio_sln',
    'fecha_fin_sln', 'fecha_inicio_ige', 'fecha_fin_ige',
    'fecha_inicio_lma', 'fecha_fin_lma', 'fecha_inicio_vac',
    'fecha_fin_vac', 'fecha_inicio_vct', 'fecha_inicio_vct',
    'fecha_inicio_irl', 'fecha_fin_irl', 'ibc_otros_parafiscales',
    'numero_horas_laboradas', 'fecha_radicacion_exterior'
]
