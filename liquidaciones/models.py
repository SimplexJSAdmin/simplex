from django.db import models

class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=75, verbose_name='Nombre de la empresa')

    def __str__(self):
        string_to_show = '{}.'.format(self.nombre_empresa)
        return string_to_show

class Periodo(models.Model):
    id_periodo = models.IntegerField(primary_key=True)
    def __str__(self):
        string_to_show = '{}'.format(self.id_periodo)
        return string_to_show

class ConceptoInterno(models.Model):
    id = models.IntegerField(primary_key=True)
    desc_concepto = models.CharField(max_length=75)


class ConceptoEmmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    desc_concepto = models.CharField(max_length=150)
    id_concepto_interno = models.ForeignKey(ConceptoInterno, on_delete=models.CASCADE)


class Topes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_tope = models.CharField(max_length=75)
    clasificacion = models.CharField(max_length=100)
    limite_superior = models.FloatField()


class Globales(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_global = models.CharField(max_length=75)
    valor = models.FloatField()


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
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    id_periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
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

