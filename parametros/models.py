from django.db import models

class Parametro(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    tipo_parametro = models.CharField(max_length=25, verbose_name='Tipo de Parametro')

    def __str__(self):
        fila = '{}: {}'.format(self.nombre, self.tipo_parametro)
        return fila

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name='nombre_empresa')


class Empleado(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id_empleado')
    empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE)
    apellido = models.CharField(max_length=50, verbose_name='apellido')
    edad = models.IntegerField(verbose_name='edad')
    nombre = models.CharField(max_length=25, verbose_name='nombre')

    def __str__(self):
        string_format = '{} {} ({})'.format(self.nombre, self.apellido, self.empresa)
        return string_format


