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

class Planta(models.Model):
    id_planta = models.AutoField(primary_key=True)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    id_periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)

