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
        exclude = ['descripcion', 'fecha']

class ReportFilter(django_filters.FilterSet):
    class Meta:
        model = Nomina
        field = '__all__'
        exclude = ['id_empresa','NIF','percalnom','area_nomina','paper','denom_periodos','periodo_inicia','fecha_inicia','tpclcnom','area_cal_nom','area_nomina2','paper2','denom_periodos2','periodo_fin','fecha_fin','tpclcnom2','idnom2','ag_pai','moneda']