from pyexpat import model
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=75, verbose_name='Nombre de la empresa')

    def __str__(self):
        string_to_show = '{}'.format(self.nombre_empresa)
        return string_to_show


class EmpresasPermitidas(models.Model):
    id = models.AutoField(primary_key=True)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class Periodo(models.Model):
    id_periodo = models.CharField(max_length=10, primary_key=True)
    meses = [
        ('01',1),
        ('02',2),
        ('03',3),
        ('04',4),
        ('05',5),
        ('06',6),
        ('07',7),
        ('08',8),
        ('09',9),
        ('10',10),
        ('11',11),
        ('12',12)
    ]
    year_periodo = models.CharField(max_length=5)
    mes_periodo = models.CharField(choices=meses, max_length=3)
    def __str__(self):
        string_to_show = '{}'.format(self.id_periodo)
        return string_to_show


class ConceptoInterno(models.Model):
    SALARIAL = 'Salarial'
    NO_SALARIAL = 'No salarial'
    id = models.AutoField(primary_key=True)
    desc_concepto = models.CharField(max_length=75)
    tipos_concepto_choices = [(SALARIAL, 'Salarial'), (NO_SALARIAL, 'No salarial')]
    tipo_concepto = models.CharField(max_length=12, choices=tipos_concepto_choices, default=SALARIAL)

    def __str__(self):
        string_to_show = 'Concepto interno: {} ({})'.format(self.desc_concepto, self.tipo_concepto)
        return string_to_show



class ConceptoEmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    desc_concepto = models.CharField(max_length=150)
    concepto_interno = models.ForeignKey(ConceptoInterno, on_delete=models.CASCADE)


class ParametrosEPS(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=150, verbose_name='Descripción del descuento por concepto de EPS')
    porcentaje_descuento_empleado = models.FloatField(verbose_name='Porcentaje de descuento empleado')
    porcentaje_descuento_empresa = models.FloatField(verbose_name='Porcentaje de descuento para la empresa')
    porcentaje_descuento_total = models.FloatField(verbose_name='Porcentaje de descuento total')
    limite_inferior = models.FloatField(verbose_name='Minima cantidad de SMMLV para el concepto')
    limite_superior = models.FloatField(verbose_name='Maxima cantidad de SMMLV para el concepto (excluyente)')


class ParametrosAFP(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=150, verbose_name='Descripción del descuento por concepto de AFP')
    porcentaje_descuento_empleado = models.FloatField(verbose_name='Porcentaje de descuento empleado')
    porcentaje_descuento_empresa = models.FloatField(verbose_name='Porcentaje de descuento para la empresa')
    porcentaje_descuento_total = models.FloatField(verbose_name='Porcentaje de descuento total')
    limite_inferior = models.FloatField(verbose_name='Minima cantidad de SMMLV para el concepto')
    limite_superior = models.FloatField(verbose_name='Maxima cantidad de SMMLV para el concepto (excluyente)')


class ParametrosFSP(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=150, verbose_name='Descripción del descuento por concepto de FSP')
    porcentaje_descuento_empleado = models.FloatField(verbose_name='Porcentaje de descuento empleado')
    porcentaje_descuento_empresa = models.FloatField(verbose_name='Porcentaje de descuento para la empresa')
    porcentaje_descuento_total = models.FloatField(verbose_name='Porcentaje de descuento total')
    limite_inferior = models.FloatField(verbose_name='Minima cantidad de SMMLV para el concepto')
    limite_superior = models.FloatField(verbose_name='Maxima cantidad de SMMLV para el concepto (excluyente)')


class ParametrosARL(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=150, verbose_name='Descripción del descuento por concepto de ARL')
    porcentaje_descuento_empleado = models.FloatField(verbose_name='Porcentaje de descuento empleado')
    porcentaje_descuento_empresa = models.FloatField(verbose_name='Porcentaje de descuento para la empresa')
    porcentaje_descuento_total = models.FloatField(verbose_name='Porcentaje de descuento total')
    nivel_riesgo = models.IntegerField(verbose_name='Nivel de riesgo para aplicar concepto')

class ParametrosSENA(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=150, verbose_name='Descripción del descuento por concepto de aportes SENA')
    porcentaje_descuento_empleado = models.FloatField(verbose_name='Porcentaje de descuento empleado')
    porcentaje_descuento_empresa = models.FloatField(verbose_name='Porcentaje de descuento para la empresa')
    porcentaje_descuento_total = models.FloatField(verbose_name='Porcentaje de descuento total')
    limite_inferior = models.FloatField(verbose_name='Minima cantidad de SMMLV para el concepto')
    limite_superior = models.FloatField(verbose_name='Maxima cantidad de SMMLV para el concepto (excluyente)')


class ParametrosICBF(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=150, verbose_name='Descripción del descuento por concepto de aportes ICBF')
    porcentaje_descuento_empleado = models.FloatField(verbose_name='Porcentaje de descuento empleado')
    porcentaje_descuento_empresa = models.FloatField(verbose_name='Porcentaje de descuento para la empresa')
    porcentaje_descuento_total = models.FloatField(verbose_name='Porcentaje de descuento total')
    limite_inferior = models.FloatField(verbose_name='Minima cantidad de SMMLV para el concepto')
    limite_superior = models.FloatField(verbose_name='Maxima cantidad de SMMLV para el concepto (excluyente)')

class ParametrosCAJA(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=150, verbose_name='Descripción del descuento por concepto de caja')
    porcentaje_descuento_empleado = models.FloatField(verbose_name='Porcentaje de descuento empleado')
    porcentaje_descuento_empresa = models.FloatField(verbose_name='Porcentaje de descuento para la empresa')
    porcentaje_descuento_total = models.FloatField(verbose_name='Porcentaje de descuento total')


class EPS(models.Model):
    id = models.AutoField(primary_key=True)
    cod_miplanilla = models.IntegerField()


class FondoPension(models.Model):
    id = models.AutoField(primary_key=True)
    cod_miplanilla = models.IntegerField()


class ARL(models.Model):
    id = models.AutoField(primary_key=True)
    cod_miplanilla = models.IntegerField()


class Planta(models.Model):
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    id_periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    no_personal = models.IntegerField()
    primer_apellido = models.CharField(max_length=75, default='')
    segundo_apellido = models.CharField(max_length=75, default='')
    primer_nombre = models.CharField(max_length=75, default='')
    segundo_nombre = models.CharField(max_length=75, default='')
    tipo_documento = models.CharField(max_length=75, default='')
    documento = models.CharField(primary_key=True, max_length=75, default='')
    division_persona = models.CharField(max_length=75, default='')
    denominacion_funcion = models.CharField(max_length=75, default='')
    und_tiempo_nomina = models.CharField(max_length=75, default='')
    cc = models.CharField(max_length=75, null=False, default='')
    cuenta_bancaria = models.CharField(max_length=75, default='')
    clase_contrato = models.CharField(max_length=75, default='')
    procedimiento_retencion = models.CharField(max_length=75, default='')
    porcentaje_retencion = models.FloatField()
    declarante_renta = models.CharField(max_length=75, default='')
    tiene_independientes = models.CharField(max_length=75, default='')
    importe = models.FloatField()
    moneda = models.CharField(max_length=75, default='')
    texto_breve = models.CharField(max_length=75, default='')
    correo_electronico = models.CharField(max_length=75, default='')
    centro_coste = models.CharField(max_length=75, default='')
    fecha = models.DateField()
    grupo_personal = models.CharField(max_length=75, default='')
    clase = models.CharField(max_length=75, default='')
    desde = models.DateField(default='')
    denominacion_posicion = models.CharField(max_length=75, default='')
    denominacion_medicion = models.CharField(max_length=75, default='')


class Nomina(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    no_personal = models.IntegerField()
    apellido_nombre = models.CharField(max_length=75)
    nombre_completo = models.CharField(max_length=75)
    NIF = models.CharField(max_length=75)
    divp = models.CharField(max_length=75)
    division_persona = models.CharField(max_length=75)
    percalnom = models.CharField(max_length=75)
    area_nomina = models.CharField(max_length=75)
    paper = models.CharField(max_length=75)
    denom_periodos = models.CharField(max_length=75)
    periodo_inicia = models.IntegerField()
    fecha_inicia = models.DateField()
    tpclcnom = models.CharField(max_length=75)
    idnom = models.CharField(max_length=75)
    area_cal_nom = models.CharField(max_length=75)
    area_nomina2 = models.CharField(max_length=75)
    paper2 = models.CharField(max_length=75)
    denom_periodos2 = models.CharField(max_length=75)
    periodo_fin = models.IntegerField()
    fecha_fin = models.DateField()
    tpclcnom2 = models.CharField(max_length=75)
    idnom2 = models.CharField(max_length=75)
    ag_pai = models.CharField(max_length=75)
    cod_concepto = models.ForeignKey(ConceptoInterno, on_delete=models.CASCADE)
    desc_concepto = models.CharField(max_length=150)
    cantidad = models.IntegerField()
    importe = models.FloatField()
    moneda = models.CharField(max_length=75)


class Liquidaciones(models.Model):
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    id_periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    estado_liquidacion = models.CharField(max_length=15, default='')
    radicado_liquidacion = models.CharField(max_length=30, default='')
    fecha_radicado_liquidacion = models.DateField()
    tipo_registro = models.CharField(max_length=2, default='02')
    secuencia = models.CharField(max_length=5, default='')
    tipo_doc_cotizante = models.CharField(max_length=2, default='')
    num_doc_cotizante = models.CharField(max_length=16, default='')
    tipo_cotizante = models.CharField(max_length=2, default='')
    subtipo_cotizante = models.CharField(max_length=2, default='')
    extranjero = models.CharField(max_length=1, default='')
    colombian_en_exterior = models.CharField(max_length=1, default='')
    cod_departamento = models.CharField(max_length=2, default='')
    cod_municipio = models.CharField(max_length=3, default='')
    primer_apellido = models.CharField(max_length=20, default='')
    segundo_apellido = models.CharField(max_length=30, default='')
    primer_nombre = models.CharField(max_length=20, default='')
    segundo_nombre = models.CharField(max_length=30, default='')
    ingreso = models.CharField(max_length=1, default='')
    retiro = models.CharField(max_length=1, default='')
    traslado_desde_eps = models.CharField(max_length=1, default='')
    traslado_hacia_eps = models.CharField(max_length=1, default='')
    traslado_desde_fondo_pension = models.CharField(max_length=1, default='')
    traslado_hacia_fondo_pension = models.CharField(max_length=1, default='')
    variacion_permanente_salario = models.CharField(max_length=1, default='')
    correcion = models.CharField(max_length=1, default='')
    variacion_transitoria_salario = models.CharField(max_length=1, default='')
    suspencion_temporal = models.CharField(max_length=1, default='')
    incapacidad_temporal = models.CharField(max_length=1, default='')
    licencia_maternidad_paternidad = models.CharField(max_length=1, default='')
    vacaciones_licencia_remunerada = models.CharField(max_length=1, default='')
    aporte_voluntario = models.CharField(max_length=1, default='')
    variacion_centros_trabajo = models.CharField(max_length=1, default='')
    dias_incapacidad = models.CharField(max_length=2, default='')
    cod_fondo_pension_pertence = models.CharField(max_length=6, default='')
    cod_fondo_pension_tralasda = models.CharField(max_length=6, default='')
    cod_eps_pertenece = models.CharField(max_length=6, default='')
    cod_eps_tralasda = models.CharField(max_length=6, default='')
    cod_ccf_pertenece = models.CharField(max_length=6, default='')
    dias_fondo_pension = models.CharField(max_length=2, default='')
    dias_eps = models.CharField(max_length=2, default='')
    dias_arl = models.CharField(max_length=2, default='')
    dias_ccf = models.CharField(max_length=2, default='')
    salario_basico = models.CharField(max_length=9, default='')
    tipo_salario = models.CharField(max_length=1, default='')
    ibc_fondo_pension = models.CharField(max_length=9, default='')
    ibc_eps = models.CharField(max_length=9, default='')
    ibc_arl = models.CharField(max_length=9, default='')
    ibc_ccf = models.CharField(max_length=9, default='')
    tarifa_fondo_pension = models.CharField(max_length=7, default='')
    cotizacion_obligatoria_pension = models.CharField(max_length=9, default='')
    aporte_voluntario_afiliado_pension = models.CharField(max_length=9, default='')
    aporte_voluntario_aportante_pension = models.CharField(max_length=9, default='')
    tota_cotizacion_pension = models.CharField(max_length=9, default='')
    aporte_fondo_solidaridad = models.CharField(max_length=9, default='')
    aporte_fondo_subsistencia = models.CharField(max_length=9, default='')
    valor_no_retenido = models.CharField(max_length=9, default='')
    tarifa_eps =models.CharField(max_length=7, default='')
    cotizacion_obligatoria_eps = models.CharField(max_length=9, default='')
    ups_adres = models.CharField(max_length=9, default='')
    autorizacion_incapacidad = models.CharField(max_length=15, default='')
    valor_incapacidad = models.CharField(max_length=9, default='')
    autorizacion_licencia_maternidad = models.CharField(max_length=15, default='')
    valor_licencia_maternidad = models.CharField(max_length=9, default='')
    tarifa_arl = models.CharField(max_length=9, default='')
    centro_trabajo = models.CharField(max_length=9, default='')
    cotizacion_obligatoria_arl = models.CharField(max_length=9, default='')
    tarifa_ccf = models.CharField(max_length=7, default='')
    valor_aporte_ccf = models.CharField(max_length=9, default='')
    tarifa_sena = models.CharField(max_length=7, default='')
    valor_aporte_sena = models.CharField(max_length=9, default='')
    tarifa_icbf = models.CharField(max_length=7, default='')
    valor_aporte_icbf = models.CharField(max_length=9, default='')
    tarifa_esap = models.CharField(max_length=7, default='')
    valor_aporte_esap = models.CharField(max_length=9, default='')
    tarifa_men = models.CharField(max_length=7, default='')
    valor_aporte_men = models.CharField(max_length=9, default='')
    tipo_doc_cotizante_principal = models.CharField(max_length=2, default='')
    numero_doc_cotizante_principal = models.CharField(max_length=16, default='')
    exonerado_pago_eps_sena_icbf = models.CharField(max_length=1, default='')
    cod_arl_pertenece = models.CharField(max_length=6, default='')
    clase_riesgo_afiliado = models.CharField(max_length=1, default='')
    indicador_tarifa_especial_pension = models.CharField(max_length=1, default='')
    fecha_ingreso = models.CharField(max_length=10, default='')
    fecha_retiro = models.CharField(max_length=10, default='')
    fecha_inicio_vsp = models.CharField(max_length=10, default='')
    fecha_inicio_sln = models.CharField(max_length=10, default='')
    fecha_fin_sln = models.CharField(max_length=10, default='')
    fecha_inicio_ige = models.CharField(max_length=10, default='')
    fecha_fin_ige = models.CharField(max_length=10, default='')
    fecha_inicio_lma = models.CharField(max_length=10, default='')
    fecha_fin_lma = models.CharField(max_length=10, default='')
    fecha_inicio_vac = models.CharField(max_length=10, default='')
    fecha_fin_vac = models.CharField(max_length=10, default='')
    fecha_inicio_vct = models.CharField(max_length=10, default='')
    fecha_inicio_vct = models.CharField(max_length=10, default='')
    fecha_inicio_irl = models.CharField(max_length=10, default='')
    fecha_fin_irl = models.CharField(max_length=10, default='')
    ibc_otros_parafiscales = models.CharField(max_length=9, default='')
    numero_horas_laboradas = models.CharField(max_length=3, default='')
    fecha_radicacion_exterior = models.CharField(max_length=10, default='')

class Log(models.Model):
    #TODO: terminar de incluir modulos disponibless
    modulos_disponibles = [('preprocesado', 'Preprocesado'), ('conceptos', 'Conceptos'), ('parametros','Parametros'),('liquidaciones','Liquidaciones'),('empresas','Empresas')]
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    module = models.CharField(choices=modulos_disponibles, max_length=30)
    fecha = models.DateTimeField()


class Preprocesamiento(models.Model):
    estados = [
        ('subidos_archivos', 'Archivos cargados al servidor'),
        ('cargando_db', 'Cargando archivos a la base de datos'),
        ('generando_liquidaciones', 'Generando las liquidaciones'),
        ('liquidacion_disponible', 'Liquidación disponible para descarga'),
        ('error_mi_planilla', 'Liquidación no ha pasado la revisión final'),
        ('exito_mi_planilla', 'Liquidación finalizada y aceptada por MiPlanilla')
    ]
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    planta = models.FileField(upload_to='path/', validators=[FileExtensionValidator(['csv'])])
    nomina = models.FileField(upload_to='path/', validators=[FileExtensionValidator(['csv'])])
    novedades  = models.FileField(upload_to='path/', validators=[FileExtensionValidator(['txt'])])
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    estado = models.CharField(choices=estados, max_length=35)
    fecha = models.DateTimeField()

class ParametrosGlobales():
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    valor = models.FloatField()
    unidad_medida = models.CharField(max_length=30)
