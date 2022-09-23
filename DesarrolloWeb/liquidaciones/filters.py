from cgitb import lookup
from dataclasses import field
import django_filters
from django_filters import DateFilter

from .models import *


class LogsFilter(django_filters.FilterSet):
    log_date = DateFilter(field_name="fecha", lookup_expr='eq')
    class Meta:
        model = Log
        fields = '__all__'
        exclude = ['descripcion', 'fecha', 'empresa']

class ReporteNomina(django_filters.FilterSet):
    class Meta:
        model = Nomina
        field = '__all__'
        exclude = ['id_empresa','NIF','percalnom','area_nomina','paper','denom_periodos','periodo_inicia','fecha_inicia','tpclcnom','area_cal_nom','area_nomina2','paper2','denom_periodos2','periodo_fin','fecha_fin','tpclcnom2','idnom2','ag_pai','moneda']

class ReportePlanta(django_filters.FilterSet):
    class Meta:
        model = Planta
        field = '__all__'
        exclude = ['id_empresa']        

class ReporteLiquidaciones(django_filters.FilterSet):
    radicado_liquidacion = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Liquidaciones
        field = '__all__'
        exclude = ['id_empresa','tipo_registro','secuencia','tipo_doc_cotizante','tipo_cotizante','subtipo_cotizante','extranjero','colombian_en_exterior','cod_departamento','cod_municipio','primer_apellido','segundo_apellido','primer_nombre','segundo_nombre','ingreso','retiro','traslado_desde_eps','traslado_hacia_eps','traslado_desde_fondo_pension','traslado_hacia_fondo_pension','variacion_permanente_salario','correcion','variacion_transitoria_salario','suspencion_temporal','incapacidad_temporal','licencia_maternidad_paternidad','vacaciones_licencia_remunerada','aporte_voluntario','variacion_centros_trabajo','dias_incapacidad','cod_fondo_pension_tralasda','cod_eps_tralasda','dias_fondo_pension','dias_eps','dias_arl','dias_ccf','tipo_salario','ibc_fondo_pension','ibc_eps','ibc_arl','ibc_ccf','tarifa_fondo_pension','cotizacion_obligatoria_pension','aporte_voluntario_afiliado_pension','aporte_voluntario_aportante_pension','tota_cotizacion_pension','aporte_fondo_solidaridad','aporte_fondo_subsistencia','valor_no_retenido','tarifa_eps','cotizacion_obligatoria_eps','ups_adres','autorizacion_incapacidad','valor_incapacidad','autorizacion_licencia_maternidad','valor_licencia_maternidad','tarifa_arl','centro_trabajo','cotizacion_obligatoria_arl','tarifa_ccf','valor_aporte_ccf','tarifa_sena','valor_aporte_sena','tarifa_icbf','valor_aporte_icbf','tarifa_esap','valor_aporte_esap','tarifa_men','valor_aporte_men','tipo_doc_cotizante_principal','numero_doc_cotizante_principal','exonerado_pago_eps_sena_icbf','cod_arl_pertenece','clase_riesgo_afiliado','indicador_tarifa_especial_pension','fecha_ingreso','fecha_retiro','fecha_inicio_vsp','fecha_inicio_sln','fecha_fin_sln','fecha_inicio_ige','fecha_fin_ige','fecha_inicio_lma','fecha_fin_lma','fecha_inicio_vac','fecha_fin_vac','fecha_inicio_vct','fecha_inicio_vct','fecha_inicio_irl','fecha_fin_irl','ibc_otros_parafiscales','numero_horas_laboradas','fecha_radicacion_exterior']