# -*- coding: utf-8 -*-
import re


class FunctionsExceptions(Exception):
    """Excepciones asociadas al módulo functions"""
    pass


class FileNotExists(FunctionsExceptions):
    """Archivo no existe"""

    def __init__(self, path: str):
        """
        Inicializa la clase

        Args:
            path (str):
                Ruta al archivo no encontrado
        """
        self.path = path

    def __str__(self):
        """
        Representación en texto de la clase
        """
        code = 'No se encontró archivo: {}'
        return code.format(self.path)


class InvalidParameterFunctions(FunctionsExceptions):
    """Parámetros invalidos"""

    def __init__(self, name: str, type_: str, others: str = None):
        """
        Inicializa la clase

        Args:
            name (str):
                Nombre del agumento o parámetro
            type_ (str):
                Tipo de datos esperado
            others (str):
                Cadena de texto con otras condiciones
        """
        self.name = name
        self.type_ = type_
        self.others = others

    def __str__(self):
        """
        Representación en texto de la clase
        """
        if self.others:
            code = 'Argumento "{}" debe ser {} y cumplir: {}'
            return code.format(self.name, self.type_, self.others)

        else:
            code = 'Argumento "{}" debe ser {}'
            return code.format(self.name, self.type_)


class InvalidOptionFunctions(FunctionsExceptions):
    """Opción inválida"""

    def __init__(self, name: str, *args):
        """
        Inicializa la clase

        Args:
            name (str):
                Nombre del agumento o parámetro
            args:
                Opciones válidas
        """
        self.name = name
        self.options = args

    def __str__(self):
        """
        Representación en texto de la clase
        """
        if len(self.options) == 0:
            code = 'Opción inválida en el parámetro "{}"'
            return code.format(self.name)

        else:
            valid_options = ''
            for opt in self.options:
                valid_options += f'{str(opt)}, '

            valid_options = re.sub(r'\,\s*$', '', str(valid_options))

            code = 'Argumento "{}" solo permite los valores {}'
            return  code.format(self.name, valid_options)


class NumberFieldIncorrect(FunctionsExceptions):
    """Número de campos no corresponde con lo esperado"""

    def __str__(self):
        """
        Representación en texto de la clase
        """
        return 'Se requieren exactamente 97 campos para generar TXT'


# -------------------------------------------------------------------
class ModelExceptions(Exception):
    """Excepciones asociadas al módulo model"""
    pass


class InvalidParameterModel(ModelExceptions):
    """Parámetros invalidos"""

    def __init__(self, name: str, type_: str):
        """
        Inicializa la clase

        Args:
            name (str):
                Nombre del agumento o parámetro
            type_ (str):
                Tipo de datos esperado
        """
        self.name = name
        self.type_ = type_

    def __str__(self):
        """
        Representación en texto de la clase
        """
        code = 'Argumento "{}" debe ser {}'
        return code.format(self.name, self.type_)


class ValueIncorrectModel(ModelExceptions):
    """Valor no permitido o incorrecto"""

    def __init__(self, name: str, condition: str):
        """
        Inicializa la clase

        Args:
            name (str):
                Nombre del agumento o parámetro
            condition (str):
                Condición que debe cumplir el argumento o parámetro
        """
        self.name = name
        self.condition = condition

    def __str__(self):
        """
        Representación en texto de la clase
        """
        code = 'Argumento "{}" debe: {}'
        return code.format(self.name, self.condition)


class WithoutData(ModelExceptions):
    """No existen datos"""

    def __init__(self, name: str):
        """
        Inicializa la clase

        Args:
            name (str):
                Nombre de la fuente de datos esperada
        """
        self.name = name

    def __str__(self):
        """
        Representación en texto de la clase
        """
        code = 'Objeto "{}" no contiene datos'
        return code.format(self.name)
