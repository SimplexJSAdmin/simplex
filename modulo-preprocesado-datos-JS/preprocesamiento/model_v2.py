# -*- coding: utf-8 -*-
from pandas.tseries.offsets import DateOffset
from decimal import Decimal
from typing import Union
from math import ceil
import pandas as pd
import re

# from .models import Empresa
# from .models import Planta
# from .models import Nomina
# from .models import Liquidacion

from .exceptions import *
from .functions import *


# -------------------------------------------------------------------
class Model():
    """Representa la lógica del modelo"""

    def __init__(self,
                 empresa: str,
                 periodo: Union[int, str] = None,
                 mes: Union[int, str] = None) -> None:
        """
        Inicializa la clase

        Args:
            empresa (str):
                Nombre de la empresa
            periodo (int, str):
                Año de la liquidación
            mes (int, str):
                Mes de la liquidación
        """
        self._fechas_anterior = None
        self._fechas_actual = None
        self._empresa = None

        # self.empresa = empresa

        self.__liquidacion_anterior = pd.DataFrame()
        self.__liquidacion_actual = pd.DataFrame()
        self.__nomina_anterior = pd.DataFrame()
        self.__planta_anterior = pd.DataFrame()
        self.__nomina_actual = pd.DataFrame()
        self.__planta_actual = pd.DataFrame()

        self._liquidacion = pd.DataFrame(columns=NAME_COLS_TXT)
        self.__empleados = None

        self.__actualizar_fechas_liquidacion(
            periodo=periodo, mes=mes
        )

    # ---------------------------------------------------------------
    @property
    def empresa(self) -> str:
        """
        Retorna el id de la empresa de la liquidación
        """
        return self._empresa

    # ---------------------------------------------------------------
    @empresa.setter
    def empresa(self, value: Union[int, str]) -> None:
        """
        Verifica que la empresa exista y asigna el id a un atributo
        de la clase

        Args:
            value (str):
                Nombre de la empresa, tal como esta registrada en
                la plataforma
        """
        if not isinstance(value, str):
            raise InvalidParameterModel('empresa', 'string')

        try:
            self._empresa = Empresa.objects.get( # noqa
                nombre_empresa = value
            ).id_empresa

        except Exception as e:
            raise ValueIncorrectModel('empresa', 'Existir en la DB')

    # ---------------------------------------------------------------
    def __actualizar_fechas_liquidacion(self, **kwargs) -> None:
        """
        Verifica y asigna las fechas requeridas para el cálculo de
        la liquidación

        Args:
            kwargs:
                Año y mes de la liquidación actual
                Admite: periodo, mes
        """
        periodo = kwargs.get('periodo', None)
        mes = kwargs.get('mes', None)

        self._fechas_anterior = generar_fechas(periodo, mes, delta_month=1)
        self._fechas_actual = generar_fechas(periodo, mes)

    # ---------------------------------------------------------------
    def generar_liquidacion(self, **kwargs) -> None:
        """
        Consolida los procesos para realizar la liquidación

        Args:
            kwargs:
                Argumento tipo diccionario para leer los archivos
                de manera local
                De la forma: Modelo = Ruta archivo
        """
        # datos de la nómina actual
        self.__nomina_actual = Data(
            'Nomina', self._fechas_actual[0], self._fechas_actual[1],
            COLS_NOMINA_ACTUAL, True, **kwargs
        ).df

        # datos de la nómina anterior
        self.__nomina_anterior = Data(
            'Nomina', self._fechas_anterior[0], self._fechas_anterior[1],
            COLS_NOMINA_ANTERIOR, False, **kwargs
        ).df

        # datos de la planta actual
        self.__planta_actual = Data(
            'Planta', self._fechas_actual[0], self._fechas_actual[1],
            COLS_PLANTA_ACTUAL, True, **kwargs
        ).df

        # datos de la planta anterior
        self.__planta_anterior = Data(
            'Planta', self._fechas_anterior[0], self._fechas_anterior[1],
            COLS_PLANTA_ANTERIOR, False, **kwargs
        ).df

        # datos de la liquidación actual
        self.__liquidacion_actual = Data(
            'Liquidacion', self._fechas_actual[0], self._fechas_actual[1],
            COLS_LIQUIDACION_ACTUAL, True, **kwargs
        ).df

        # datos de la liquidación anterior
        self.__liquidacion_anterior = Data(
            'Liquidacion', self._fechas_anterior[0], self._fechas_anterior[1],
            COLS_LIQUIDACION_ANTERIOR, False, **kwargs
        ).df

        # lista de empleados únicos
        self.__empleados = self.__obtener_lista_empleados()

        # consolidación de los registros
        df_empleados = self.__consolidar_empleados(
            self.__nomina_actual, self.__planta_actual, self.__liquidacion_actual,
            self.__nomina_anterior, self.__planta_anterior, self.__liquidacion_anterior
        )

        reporte_txt = []

        for idx, empleado in enumerate(self.__empleados):
            # información
            print(f'{idx + 1} de {len(self.__empleados)}')

            # datos del empleado
            df_empleado_nomina_actual = df_empleados['nomina_actual']
            df_empleado_nomina_actual = df_empleado_nomina_actual[
                df_empleado_nomina_actual.no_personal == empleado
            ].copy()

            df_empleado_nomina_anterior = df_empleados['nomina_anterior']
            df_empleado_nomina_anterior = df_empleado_nomina_anterior[
                df_empleado_nomina_anterior.no_personal == empleado
            ].copy()

            df_empleado_planta_actual = df_empleados['planta_actual']
            df_empleado_planta_actual = df_empleado_planta_actual[
                df_empleado_planta_actual.no_personal == empleado
            ].copy()

            df_empleado_planta_anterior = df_empleados['planta_anterior']
            df_empleado_planta_anterior = df_empleado_planta_anterior[
                df_empleado_planta_anterior.no_personal == empleado
            ].copy()

            df_empleado_liquidacion_actual = df_empleados['liquidacion_actual']
            df_empleado_liquidacion_actual = df_empleado_liquidacion_actual[
                df_empleado_liquidacion_actual.no_personal == empleado
            ].copy()

            df_empleado_liquidacion_anterior = df_empleados['liquidacion_anterior']
            df_empleado_liquidacion_anterior = df_empleado_liquidacion_anterior[
                df_empleado_liquidacion_anterior.no_personal == empleado
            ].copy()

            # se define secuencia del registro
            secuencia = idx + 1

            # liquidación
            liquidacion_empleado = Liquidacion(
                empleado,
                secuencia,
                df_empleado_nomina_actual,
                df_empleado_planta_actual,
                df_empleado_liquidacion_actual,
                df_empleado_nomina_anterior,
                df_empleado_planta_anterior,
                df_empleado_liquidacion_anterior,
                self._fechas_actual[0],
                self._fechas_actual[1],
                True
            )

            if liquidacion_empleado.data:
                reporte_txt.append(*liquidacion_empleado.data)

            # eliminación de objetos
            del df_empleado_nomina_actual
            del df_empleado_planta_actual
            del df_empleado_liquidacion_actual
            del df_empleado_nomina_anterior
            del df_empleado_planta_anterior
            del df_empleado_liquidacion_anterior
            del liquidacion_empleado

        self._liquidacion = pd.DataFrame(reporte_txt, columns=NAME_COLS_TXT)
        self._guardar(kwargs.get('PATH'))

    # ---------------------------------------------------------------
    def __obtener_lista_empleados(self, key: str = 'no_personal') -> list:
        """
        Obtiene la lista de empleados únicos

        Args:
            key (str):
                Campos clave para obtener el ID de los empleados

        Return:
            Lista con los ID únicos de los empleados
        """
        if self.__nomina_actual.empty:
            raise WithoutData('nomina')

        if not isinstance(self.__nomina_actual, pd.DataFrame):
            raise InvalidParameterModel('nomina', 'Dataframe pandas')

        if not isinstance(key, str):
            raise InvalidParameterModel('key', 'String')

        else:
            try:
                assert key in self.__nomina_actual.columns, f'key={key} no existe'

            except AssertionError:
                self.__nomina_actual = self.__nomina_actual.rename(columns={
                    'Nº pers.': 'no_personal'
                })

        return self.__nomina_actual['no_personal'].unique().tolist()

    # ---------------------------------------------------------------
    def __consolidar_empleados(self,
                               nomina_actual: pd.DataFrame,
                               planta_actual: pd.DataFrame,
                               liquidacion_actual: pd.DataFrame,
                               nomina_anterior: pd.DataFrame,
                               planta_anterior: pd.DataFrame,
                               liquidacion_anterior: pd.DataFrame) -> list:
        """
        Combina las fuentes de datos para crear un único
        dataframe con los datos requeridos para la generación del TXT

        Args:
            nomina_actual (pd.DataFrame):
                Datos de nómina actual del empleado
            planta_actual (pd.DataFrame):
                Datos de planta antual del empleado
            liquidacion_actual (pd.DataFrame):
                Datos de la liquidación actual del empleado
            nomina_anterior (pd.DataFrame):
                Datos de nómina anterior del empleado
            planta_anterior (pd.DataFrame):
                Datos de planta antual del empleado
            liquidacion_anterior (pd.DataFrame):
                Datos de la liquidación anterior del empleado

        Return:
            Dataframe pandas
        """
        # seleccionar columnas para relacionar casos
        ids = planta_actual.loc[:, ['no_personal', 'documento']]

        # tipo de novedad
        info_conceptos = pd.DataFrame(INFO_CONCEPTOS)

        # joins
        try:
            nomina_actual = pd.merge(
                nomina_actual, ids, on='no_personal', how='left'
            )
        except TypeError:
            pass

        try:
            nomina_actual = pd.merge(
                nomina_actual, info_conceptos, on='cod_concepto', how='left'
            )
        except TypeError:
            pass

        try:
            nomina_anterior = pd.merge(
                nomina_anterior, ids, on='no_personal', how='left'
            )
        except TypeError:
            pass

        try:
            nomina_anterior = pd.merge(
                nomina_anterior, info_conceptos, on='cod_concepto', how='left'
            )
        except TypeError:
            pass

        try:
            liquidacion_actual = pd.merge(
                liquidacion_actual, ids, left_on='num_doc_cotizante', right_on='documento', how='left'
            )
        except TypeError:
            pass

        try:
            liquidacion_anterior = pd.merge(
                liquidacion_anterior, ids, left_on='num_doc_cotizante', right_on='documento', how='left'
            )
        except TypeError:
            pass

        # ajuste de dtypes
        nomina_actual.cantidad = pd.to_numeric(nomina_actual.cantidad)
        nomina_actual.importe = pd.to_numeric(nomina_actual.importe)

        if isinstance(nomina_anterior, pd.DataFrame):
            nomina_anterior.cantidad = pd.to_numeric(nomina_anterior.cantidad)
            nomina_anterior.importe = pd.to_numeric(nomina_anterior.importe)

        planta_actual.importe = pd.to_numeric(planta_actual.importe)

        if isinstance(planta_anterior, pd.DataFrame):
            planta_anterior.importe = pd.to_numeric(planta_anterior.importe)

        liquidacion_actual.tipo_cotizante = pd.to_numeric(liquidacion_actual.tipo_cotizante)
        liquidacion_actual.clase_riesgo_afiliado = pd.to_numeric(liquidacion_actual.clase_riesgo_afiliado)
        liquidacion_actual.centro_trabajo = pd.to_numeric(liquidacion_actual.centro_trabajo)

        if isinstance(liquidacion_anterior, pd.DataFrame):
            liquidacion_anterior.clase_riesgo_afiliado = pd.to_numeric(liquidacion_anterior.clase_riesgo_afiliado)
            liquidacion_anterior.centro_trabajo = pd.to_numeric(liquidacion_anterior.centro_trabajo)

        # diccionario con los dataframes
        data = {
            'nomina_actual': nomina_actual,
            'nomina_anterior': nomina_anterior,
            'planta_actual': planta_actual,
            'planta_anterior': planta_anterior,
            'liquidacion_actual': liquidacion_actual,
            'liquidacion_anterior': liquidacion_anterior,
        }

        return data

    # ---------------------------------------------------------------
    def _guardar(self, path: str = None) -> None:
        """
        Guarda el resultado de la liquidación en la DB o en un
        archivo local

        Args:
            path (str):
                Ruta para almacenar archivo, si es None lo guarda
                en la base de datos de la plataforma
        """
        if path:
            self._liquidacion.to_csv(path, index=False)

        else:
            print(self._liquidacion)
            return self._liquidacion


# -------------------------------------------------------------------
class Liquidacion():

    def __init__(self,
                 id_empleado: str,
                 secuencia: int,
                 nomina_actual: pd.DataFrame,
                 planta_actual: pd.DataFrame,
                 liquidacion_actual: pd.DataFrame,
                 nomina_anterior: pd.DataFrame,
                 planta_anterior: pd.DataFrame,
                 liquidacion_anterior: pd.DataFrame,
                 fecha_inicio: pd.Timestamp,
                 fecha_final: pd.Timestamp,
                 imprimir_resumen: bool = False) -> None:
        """
        Inicializa la clase

        Args:
            id_empleado ():
                ID del empleado
            secuencia (int):
                Consecutivo entero para el empleado
            nomina_actual (pd.DataFrame):
                Datos de nómina actual del empleado
            planta_actual (pd.DataFrame):
                Datos de planta antual del empleado
            liquidacion_actual (pd.DataFrame):
                Datos de la liquidación actual del empleado
            nomina_anterior (pd.DataFrame):
                Datos de nómina anterior del empleado
            planta_anterior (pd.DataFrame):
                Datos de planta antual del empleado
            liquidacion_anterior (pd.DataFrame):
                Datos de la liquidación anterior del empleado
            fecha_inicio (timestamp):
                Fecha de inicio del reporte de liquidación
            fecha_final (timestamp):
                Fecha de finalización del reporte de liquidación
            imprimir_resumen (bool):
                Indica si se debe mostrar por pantalla un resumen
                del proceso por empleado
        """
        self.fecha_inicio_informe = pd.Timestamp(fecha_inicio)
        self.fecha_fin_informe = pd.Timestamp(fecha_final)
        self.imprimir_resumen = imprimir_resumen
        self.id_empleado = id_empleado
        self.__data = []

        self.secuencia = secuencia

        self.nomina_actual = nomina_actual
        self.planta_actual = planta_actual
        self.liquidacion_actual = liquidacion_actual
        self.nomina_anterior = nomina_anterior
        self.planta_anterior = planta_anterior
        self.liquidacion_anterior = liquidacion_anterior

        self.info_ibc_empleado = None
        self.info_txt_empleado = []

        self.liquidacion_simple = self.__es_liquidacion_simple()

        # ejecución de la liquidación
        self.liquidar()

    # ---------------------------------------------------------------
    @property
    def data(self) -> pd.DataFrame:
        """
        Retorna el resultado de la liquidación

        Return:
            Dataframe pandas
        """
        return self.__data

    # ---------------------------------------------------------------
    def __len__(self) -> str:
        """
        Se rediseña método para mostrar el número de campos
        disponibles para el cálculo del TXT del empleado

        Return:
            Entero
        """
        return len(self.info_txt_empleado)

    # ---------------------------------------------------------------
    def liquidar(self, full: bool = False):
        """
        Ejecuta el proceso de liquidación del empleado y ejecuta
        el método correspondiente
        """
        if self.liquidacion_simple:
            self.__caso_simple()

        else:
            self.__caso_complejo()

        # if self.imprimir_resumen:
        #         tmp = generar_linea_txt(*self.info_txt_empleado[0])

        #         if full:
        #             print(self.info_ibc_empleado)
        #             print('\n{}'.format('*'*80))
        #             print(f'|{tmp}|')
        #             print('{}'.format('*'*80))

        #         else:
        #             print(f'{tmp}|')

        self.__data = self.info_txt_empleado

    # ---------------------------------------------------------------
    def __es_liquidacion_simple(self) -> bool:
        """
        Determina si es una liquidación simple

        Return:
            True si la liquidación no contiene conceptos que la
            hagan una liquidación especial, en cuyo caso se
            retorna la lista con los conceptos que aplican
        """
        if not isinstance(self.nomina_actual, pd.DataFrame):
            raise InvalidParameterModel('nomina_actual', 'dataframe pandas')

        conceptos_empleado = self.nomina_actual.cod_concepto.unique().tolist()

        cods_casos_especiales = CONCEPTOS_INCAPACIDADES\
                                + CONCEPTOS_LICENCIAS \
                                + CONCEPTOS_VACACIONES

        for c in conceptos_empleado:
            if c in cods_casos_especiales:
                return False

        return True

    # ---------------------------------------------------------------
    def __campos_txt_empleado_simple(self, **kwargs) -> None:
        """
        Busca y almacena los campos requeridos para generar la
        información del empleado en el TXT

        Args:
            kwargs:
                Indica el tipo de novedad que se va a calcular
                y que no requiere nueva linea
        """
        # lista vacía que almacena los datos de una línea del txt
        campos_txt = []

        campos_txt.append(
            self.liquidacion_actual.tipo_registro.iloc[0]
        )
        campos_txt.append(
            self.secuencia
        )
        campos_txt.append(
            self.liquidacion_actual.tipo_doc_cotizante.iloc[0].upper()
        )
        campos_txt.append(
            self.planta_actual.documento.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.tipo_cotizante.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.subtipo_cotizante.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.extranjero.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.colombian_en_exterior.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.cod_departamento.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.cod_municipio.iloc[0]
        )
        campos_txt.append(
            self.planta_actual.primer_apellido.iloc[0].upper()
        )
        campos_txt.append(
            self.planta_actual.segundo_apellido.iloc[0].upper()
        )
        campos_txt.append(
            self.planta_actual.primer_nombre.iloc[0].upper()
        )
        campos_txt.append(
            self.planta_actual.segundo_nombre.iloc[0].upper()
        )

        # novedades de contratación y retiro
        if self.info_ibc_empleado.status_ingreso:
            campos_txt.append('X')
        else:
            campos_txt.append('')

        if self.info_ibc_empleado.status_retiro:
            campos_txt.append('X')
        else:
            campos_txt.append('')

        # novedades de traslados
        campos_txt.append(
            self.liquidacion_actual.traslado_desde_eps.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.traslado_hacia_eps.iloc[0]
        )

        if self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_lectivo:
            campos_txt.append('')
            campos_txt.append('')
        else:
            campos_txt.append(
                self.liquidacion_actual.traslado_desde_fondo_pension.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.traslado_hacia_fondo_pension.iloc[0]
            )

        # otras novedades
        novedad_vsp = False
        try:
            if self.planta_actual.importe.iloc[0] != self.planta_anterior.importe.iloc[0]:
                novedad_vsp = True
        except IndexError:
            pass

        if novedad_vsp:
            campos_txt.append('X')
        else:
            campos_txt.append('')

        campos_txt.append(
            self.liquidacion_actual.correcion.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.variacion_transitoria_salario.iloc[0]
        )

        # suspensión temporal - sln
        if kwargs.get('novedad', '') == 'sln':
            campos_txt.append('X')
        else:
            campos_txt.append('')

        campos_txt.append(
            self.liquidacion_actual.incapacidad_temporal.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.licencia_maternidad_paternidad.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.vacaciones_licencia_remunerada.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.aporte_voluntario.iloc[0]
        )

        try:
            ct_0 = self.liquidacion_anterior.centro_trabajo.drop_duplicates().iloc[0]
            tr_0 = self.liquidacion_anterior.clase_riesgo_afiliado.drop_duplicates().iloc[0]
            tc_0 = self.liquidacion_anterior.tipo_cotizante.drop_duplicates().iloc[0]

            ct_1 = self.liquidacion_actual.centro_trabajo.drop_duplicates().iloc[0]
            tr_1 = self.liquidacion_actual.clase_riesgo_afiliado.drop_duplicates().iloc[0]
            tc_1 = self.liquidacion_actual.tipo_cotizante.drop_duplicates().iloc[0]

        except Exception:
            campos_txt.append('')
        else:
            if (ct_0 != ct_1) and (tr_0 != tr_1):
                if tc_0 == 12 and tc_1 == 19:
                    campos_txt.append('')
                else:
                    campos_txt.append('X')
            else:
                campos_txt.append('')

        # días de incapacidad
        campos_txt.append(
            self.liquidacion_actual.dias_incapacidad.iloc[0]
        )

        # entidades
        campos_txt.append(
            self.liquidacion_actual.cod_fondo_pension_pertence.iloc[0].upper()
        )
        campos_txt.append(
            self.liquidacion_actual.cod_fondo_pension_tralasda.iloc[0].upper()
        )
        campos_txt.append(
            self.liquidacion_actual.cod_eps_pertenece.iloc[0].upper()
        )
        campos_txt.append(
            self.liquidacion_actual.cod_eps_tralasda.iloc[0].upper()
        )
        campos_txt.append(
            self.liquidacion_actual.cod_ccf_pertenece.iloc[0].upper()
        )

        # días de cotización
        if self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
            campos_txt.append(0)
        else:
            campos_txt.append(
                self.liquidacion_actual.dias_fondo_pension.iloc[0]
            )

        campos_txt.append(
            self.liquidacion_actual.dias_eps.iloc[0]
        )

        campos_txt.append(
            self.liquidacion_actual.dias_arl.iloc[0]
        )

        if self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
            campos_txt.append(0)
        else:
            campos_txt.append(
                self.liquidacion_actual.dias_ccf.iloc[0]
            )

        # información salarial
        campos_txt.append(
            self.info_ibc_empleado.salario_empleado_30_dias
        )
        campos_txt.append(
            self.liquidacion_actual.tipo_salario.iloc[0].upper()
        )

        # información ibc
        campos_txt.append(
            self.info_ibc_empleado['pension']
        )
        campos_txt.append(
            self.info_ibc_empleado['salud']
        )
        campos_txt.append(
            self.info_ibc_empleado['riesgos']
        )
        campos_txt.append(
            self.info_ibc_empleado['ccf']
        )

        # cotización pensión
        if self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo or self.info_ibc_empleado.es_pensionado_activo:
            campos_txt.append(0)
            campos_txt.append(0)
            campos_txt.append(0)
            campos_txt.append(0)
            campos_txt.append(0)

        else:
            tmp_porc_pension = PORC_PENSION_TOTAL

            if kwargs.get('novedades', '') == 'sln':
                tmp_porc_pension = PORC_PENSION_EMPLEADOR

            campos_txt.append(
                tmp_porc_pension
            )
            campos_txt.append(
                round_100(self.info_ibc_empleado['pension'] * tmp_porc_pension)
            )
            campos_txt.append(
                self.liquidacion_actual.aporte_voluntario_afiliado_pension.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.aporte_voluntario_aportante_pension.iloc[0]
            )
            campos_txt.append(
                round_100(sumar(*campos_txt[46:48]))
            )

        # aporte de solidaridad
        # ley 797/2003
        tmp_pension = self.info_ibc_empleado['pension']
        if tmp_pension >= TOPE_MINIMO_FONDO_SOLIDARIDAD_SMMLV:
            campos_txt.append(
                round_100(tmp_pension * PORC_FSP)
            )
        else:
            campos_txt.append(0)

        # aporte al fondo de subsistencia
        # art. 8 - ley 797/2003
        if tmp_pension >= TOPE_MINIMO_FONDO_SUBSISTENCIA_SMMLV:
            if tmp_pension <= TOPE_2_FONDO_SUBSISTENCIA_SMMLV:
                campos_txt.append(round_100(tmp_pension * PORC_FS))

            elif tmp_pension <= TOPE_3_FONDO_SUBSISTENCIA_SMMLV:
                campos_txt.append(round_100(tmp_pension * PORC_TOPE_2))

            elif tmp_pension <= TOPE_4_FONDO_SUBSISTENCIA_SMMLV:
                campos_txt.append(round_100(tmp_pension * PORC_TOPE_3))

            elif tmp_pension <= TOPE_5_FONDO_SUBSISTENCIA_SMMLV:
                campos_txt.append(round_100(tmp_pension * PORC_TOPE_4))

            elif tmp_pension <= TOPE_6_FONDO_SUBSISTENCIA_SMMLV:
                campos_txt.append(round_100(tmp_pension * PORC_TOPE_5))

            else:
                campos_txt.append(round_100(tmp_pension * PORC_TOPE_6))

        else:

            campos_txt.append(0)

        # valor no retenido
        # se confirma campo en desuso por parte de Sicard - 20/sep
        campos_txt.append(0)

        # cotización salud
        if self.info_ibc_empleado['salud'] > TOPE_CAMBIO_PERC_SALUD:
            tmp_salud = PORC_SALUD_EMPLEADO_INT
        elif self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
            tmp_salud = PORC_SALUD_EMPLEADO_INT
        else:
            tmp_salud = PORC_SALUD_EMPLEADO_BAS

        campos_txt.append(
            tmp_salud
        )

        campos_txt.append(
            round_100(self.info_ibc_empleado['salud'] * tmp_salud)
        )

        # valor upc
        # se confirma campo en desuso por parte de Sicard - 20/sep
        campos_txt.append(0)

        # información novedades
        campos_txt.append(
            self.liquidacion_actual.autorizacion_incapacidad.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.valor_incapacidad.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.autorizacion_licencia_maternidad.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.valor_licencia_maternidad.iloc[0]
        )

        # cotización arl
        tipo_riesgo = self.liquidacion_actual.clase_riesgo_afiliado.iloc[0]
        porc_riesgo = 0

        if tipo_riesgo == 1:
            porc_riesgo = PORC_ARL_I
        elif tipo_riesgo == 2:
            porc_riesgo = PORC_ARL_II
        elif tipo_riesgo == 3:
            porc_riesgo = PORC_ARL_III
        elif tipo_riesgo == 4:
            porc_riesgo = PORC_ARL_IV
        elif tipo_riesgo == 5:
            porc_riesgo = PORC_ARL_V

        if kwargs.get('novedad', '') == 'sln':
            porc_riesgo = 0

        campos_txt.append(
                porc_riesgo
        )

        campos_txt.append(
            self.liquidacion_actual.centro_trabajo.iloc[0]
        )
        campos_txt.append(
            round_100(self.info_ibc_empleado['riesgos'] * porc_riesgo)
        )

        # caja de compensación familiar
        if self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
            campos_txt.append(0)
        else:
            campos_txt.append(
                PORC_CCF
            )

        campos_txt.append(
            round_100(self.info_ibc_empleado['ccf'] * campos_txt[63])
        )

        # parafiscales
        excepto_parafiscales = True
        if self.info_ibc_empleado['salud'] >= self.info_ibc_empleado.salario_integral:
            excepto_parafiscales = False
        elif self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
            excepto_parafiscales = False

        if excepto_parafiscales or self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
            campos_txt.append(0)
        else:
            campos_txt.append(PORC_SENA)

        campos_txt.append(
            round_100(self.info_ibc_empleado['sena'] * campos_txt[65])
        )

        if excepto_parafiscales or self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
            campos_txt.append(0)
        else:
            campos_txt.append(PORC_ICBF)

        campos_txt.append(
            round_100(self.info_ibc_empleado['icbf'] * campos_txt[67])
        )

        # valor de novedades - esap
        # se confirma campo en desuso por parte de Sicard - 20/sep
        campos_txt.append(0)
        campos_txt.append(0)

        # valor de novedades - men
        # se confirma campo en desuso por parte de Sicard - 20/sep
        campos_txt.append(0)
        campos_txt.append(0)

        # información adicional
        campos_txt.append(
            self.liquidacion_actual.tipo_doc_cotizante_principal.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.numero_doc_cotizante_principal.iloc[0]
        )

        # excepción de pago eps y parafiscales
        if excepto_parafiscales:
            campos_txt.append('S')
        else:
            campos_txt.append('N')

        # información adicional de riesgos laborales
        campos_txt.append(
            self.liquidacion_actual.cod_arl_pertenece.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.clase_riesgo_afiliado.iloc[0]
        )

        # tarifa especial de pensión
        # se confirma campo no aplica por parte de Sicard - 20/sep
        campos_txt.append('')

        # fechas de novedades
        if self.info_ibc_empleado.status_ingreso:
            campos_txt.append(
                self.planta_actual.desde.iloc[0].strftime('%Y-%m-%d')
            )
        else:
            campos_txt.append('')

        # retiro aplica desde el día anterior
        if self.info_ibc_empleado.status_retiro:
            campos_txt.append(
                (self.planta_actual.desde.iloc[0] - DateOffset(days=1)).strftime('%Y-%m-%d')
            )
        else:
            campos_txt.append('')

        if novedad_vsp:
            if self.info_ibc_empleado.status_retiro:
                campos_txt.append(self.planta_anterior.desde.iloc[0].strftime('%Y-%m-%d'))
            else:
                campos_txt.append(self.planta_actual.desde.iloc[0].strftime('%Y-%m-%d'))
        else:
            campos_txt.append('')

        campos_txt.append(
            self.liquidacion_actual.fecha_inicio_sln.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_fin_sln.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_inicio_ige.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_fin_ige.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_inicio_lma.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_fin_lma.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_inicio_vac.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_fin_vac.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_inicio_vct.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_inicio_vct.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_inicio_irl.iloc[0]
        )
        campos_txt.append(
            self.liquidacion_actual.fecha_fin_irl.iloc[0]
        )

        # ibc parafiscales
        campos_txt.append(
            self.info_ibc_empleado['sena']
        )

        # horas laboradas
        if INCLUIR_HORAS_DIA:
            campos_txt.append(
                self.info_ibc_empleado.dias_pagos_salariales * HORAS_POR_DIA
            )
        else:
            campos_txt.append(0)

        # fecha de radicación en el exterior
        campos_txt.append(
            self.liquidacion_actual.fecha_radicacion_exterior.iloc[0]
        )

        # agregar información a la lista principal
        self.info_txt_empleado.append(campos_txt)

    # ---------------------------------------------------------------
    def __caso_simple(self) -> None:
        """
        Ejecuta la liquidación para un caso simple y asigna el resultado
        a la propiedad data de la clase
        """
        self.info_ibc_empleado = IBC(
            id_empleado=self.id_empleado,
            fecha_inicio=self.fecha_inicio_informe,
            fecha_final=self.fecha_fin_informe,
            nomina_actual=self.nomina_actual,
            planta_actual=self.planta_actual,
            planta_anterior=self.planta_anterior,
            liquidacion_actual=self.liquidacion_actual
        )

        self.__campos_txt_empleado_simple()

    # ---------------------------------------------------------------
    def __caso_complejo(self) -> bool:
        """
        Ejecuta la liquidación para un caso complejo y asigna el resultado
        a la propiedad data de la clase
        """
        self.info_ibc_empleado = IBC(
            id_empleado=self.id_empleado,
            fecha_inicio=self.fecha_inicio_informe,
            fecha_final=self.fecha_fin_informe,
            nomina_actual=self.nomina_actual,
            nomina_anterior=self.nomina_anterior,
            planta_actual=self.planta_actual,
            planta_anterior=self.planta_anterior,
            liquidacion_actual=self.liquidacion_actual,
            caso_especial_ibc=True
        )

        self.__campos_txt_empleado_simple()

        # verifica novedad sln
        # nov_sln_empleado = []
        # for c in CONCEPTOS_SLN:
        #     if c in self.info_ibc_empleado.conceptos_empleados_actual:
        #         if self.nomina_actual[self.nomina_actual.cod_concepto == c].cantidad.iloc[0] == 30:
        #             self.__campos_txt_empleado_simple(novedad='sln')
        #         else:
        #             pass
        #             #self.__campos_txt_empleado_complejo_sln()

    # ---------------------------------------------------------------
    def __campos_txt_empleado_complejo_sln(self, concepto_sln: str) -> None:
        """
        Busca y almacena los campos requeridos para generar la
        información del empleado en el TXT asociado al SLN

        Args:
            concepto_sln (str):
                Código del concepto SLN a calcular
        """
        # verifica si se requiere una o dos lineas para novedad SLN
        dias_sln = self.nomina_actual[self.nomina_actual.cod_concepto == concepto_sln].cantidad.iloc[0]

        # lista vacía que almacena los datos de una línea del txt
        if dias_sln == 30:
            campos_txt = []

            campos_txt.append(
                self.liquidacion_actual.tipo_registro.iloc[0]
            )
            campos_txt.append(
                self.secuencia
            )
            campos_txt.append(
                self.liquidacion_actual.tipo_doc_cotizante.iloc[0].upper()
            )
            campos_txt.append(
                self.planta_actual.documento.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.tipo_cotizante.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.subtipo_cotizante.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.extranjero.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.colombian_en_exterior.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.cod_departamento.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.cod_municipio.iloc[0]
            )
            campos_txt.append(
                self.planta_actual.primer_apellido.iloc[0].upper()
            )
            campos_txt.append(
                self.planta_actual.segundo_apellido.iloc[0].upper()
            )
            campos_txt.append(
                self.planta_actual.primer_nombre.iloc[0].upper()
            )
            campos_txt.append(
                self.planta_actual.segundo_nombre.iloc[0].upper()
            )

            # novedades de contratación y retiro
            if self.info_ibc_empleado.status_ingreso:
                campos_txt.append('X')
            else:
                campos_txt.append('')

            if self.info_ibc_empleado.status_retiro:
                campos_txt.append('X')
            else:
                campos_txt.append('')

            # novedades de traslados
            campos_txt.append(
                self.liquidacion_actual.traslado_desde_eps.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.traslado_hacia_eps.iloc[0]
            )

            if self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_lectivo:
                campos_txt.append('')
                campos_txt.append('')
            else:
                campos_txt.append(
                    self.liquidacion_actual.traslado_desde_fondo_pension.iloc[0]
                )
                campos_txt.append(
                    self.liquidacion_actual.traslado_hacia_fondo_pension.iloc[0]
                )

            # otras novedades
            novedad_vsp = False
            try:
                if self.planta_actual.importe.iloc[0] != self.planta_anterior.importe.iloc[0]:
                    novedad_vsp = True
            except IndexError:
                pass

            if novedad_vsp:
                campos_txt.append('X')
            else:
                campos_txt.append('')

            campos_txt.append(
                self.liquidacion_actual.correcion.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.variacion_transitoria_salario.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.suspencion_temporal.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.incapacidad_temporal.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.licencia_maternidad_paternidad.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.vacaciones_licencia_remunerada.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.aporte_voluntario.iloc[0]
            )

            try:
                ct_0 = self.liquidacion_anterior.centro_trabajo.drop_duplicates().iloc[0]
                tr_0 = self.liquidacion_anterior.clase_riesgo_afiliado.drop_duplicates().iloc[0]
                tc_0 = self.liquidacion_anterior.tipo_cotizante.drop_duplicates().iloc[0]

                ct_1 = self.liquidacion_actual.centro_trabajo.drop_duplicates().iloc[0]
                tr_1 = self.liquidacion_actual.clase_riesgo_afiliado.drop_duplicates().iloc[0]
                tc_1 = self.liquidacion_actual.tipo_cotizante.drop_duplicates().iloc[0]

            except Exception:
                campos_txt.append('')
            else:
                if (ct_0 != ct_1) and (tr_0 != tr_1):
                    if tc_0 == 12 and tc_1 == 19:
                        campos_txt.append('')
                    else:
                        campos_txt.append('X')
                else:
                    campos_txt.append('')

            # días de incapacidad
            campos_txt.append(
                self.liquidacion_actual.dias_incapacidad.iloc[0]
            )

            # entidades
            campos_txt.append(
                self.liquidacion_actual.cod_fondo_pension_pertence.iloc[0].upper()
            )
            campos_txt.append(
                self.liquidacion_actual.cod_fondo_pension_tralasda.iloc[0].upper()
            )
            campos_txt.append(
                self.liquidacion_actual.cod_eps_pertenece.iloc[0].upper()
            )
            campos_txt.append(
                self.liquidacion_actual.cod_eps_tralasda.iloc[0].upper()
            )
            campos_txt.append(
                self.liquidacion_actual.cod_ccf_pertenece.iloc[0].upper()
            )

            # días de cotización
            if self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
                campos_txt.append(0)
            else:
                campos_txt.append(
                    self.liquidacion_actual.dias_fondo_pension.iloc[0]
                )

            campos_txt.append(
                self.liquidacion_actual.dias_eps.iloc[0]
            )

            campos_txt.append(
                self.liquidacion_actual.dias_arl.iloc[0]
            )

            if self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
                campos_txt.append(0)
            else:
                campos_txt.append(
                    self.liquidacion_actual.dias_ccf.iloc[0]
                )

            # información salarial
            campos_txt.append(
                self.info_ibc_empleado.salario_empleado_30_dias
            )
            campos_txt.append(
                self.liquidacion_actual.tipo_salario.iloc[0].upper()
            )

            # información ibc
            campos_txt.append(
                self.info_ibc_empleado['pension']
            )
            campos_txt.append(
                self.info_ibc_empleado['salud']
            )
            campos_txt.append(
                self.info_ibc_empleado['riesgos']
            )
            campos_txt.append(
                self.info_ibc_empleado['ccf']
            )

            # cotización pensión
            if self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo or self.info_ibc_empleado.es_pensionado_activo:
                campos_txt.append(0)
                campos_txt.append(0)
                campos_txt.append(0)
                campos_txt.append(0)
                campos_txt.append(0)

            else:
                campos_txt.append(
                    PORC_PENSION_EMPLEADO
                )
                campos_txt.append(
                    round_100(self.info_ibc_empleado['pension'] * PORC_PENSION_EMPLEADO)
                )
                campos_txt.append(
                    self.liquidacion_actual.aporte_voluntario_afiliado_pension.iloc[0]
                )
                campos_txt.append(
                    self.liquidacion_actual.aporte_voluntario_aportante_pension.iloc[0]
                )
                campos_txt.append(
                    round_100(sumar(*campos_txt[46:48]))
                )

            # aporte de solidaridad
            # ley 797/2003
            tmp_pension = self.info_ibc_empleado['pension']
            if tmp_pension >= TOPE_MINIMO_FONDO_SOLIDARIDAD_SMMLV:
                campos_txt.append(
                    round_100(tmp_pension * PORC_FSP)
                )
            else:
                campos_txt.append(0)

            # aporte al fondo de subsistencia
            # art. 8 - ley 797/2003
            if tmp_pension >= TOPE_MINIMO_FONDO_SUBSISTENCIA_SMMLV:
                if tmp_pension <= TOPE_2_FONDO_SUBSISTENCIA_SMMLV:
                    campos_txt.append(round_100(tmp_pension * PORC_FS))

                elif tmp_pension <= TOPE_3_FONDO_SUBSISTENCIA_SMMLV:
                    campos_txt.append(round_100(tmp_pension * PORC_TOPE_2))

                elif tmp_pension <= TOPE_4_FONDO_SUBSISTENCIA_SMMLV:
                    campos_txt.append(round_100(tmp_pension * PORC_TOPE_3))

                elif tmp_pension <= TOPE_5_FONDO_SUBSISTENCIA_SMMLV:
                    campos_txt.append(round_100(tmp_pension * PORC_TOPE_4))

                elif tmp_pension <= TOPE_6_FONDO_SUBSISTENCIA_SMMLV:
                    campos_txt.append(round_100(tmp_pension * PORC_TOPE_5))

                else:
                    campos_txt.append(round_100(tmp_pension * PORC_TOPE_6))

            else:

                campos_txt.append(0)

            # valor no retenido
            # se confirma campo en desuso por parte de Sicard - 20/sep
            campos_txt.append(0)

            # cotización salud
            if self.info_ibc_empleado['salud'] > TOPE_CAMBIO_PERC_SALUD:
                tmp_salud = PORC_SALUD_EMPLEADO_INT
            elif self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
                tmp_salud = PORC_SALUD_EMPLEADO_INT
            else:
                tmp_salud = PORC_SALUD_EMPLEADO_BAS

            campos_txt.append(
                tmp_salud
            )

            campos_txt.append(
                round_100(self.info_ibc_empleado['salud'] * tmp_salud)
            )

            # valor upc
            # se confirma campo en desuso por parte de Sicard - 20/sep
            campos_txt.append(0)

            # información novedades
            campos_txt.append(
                self.liquidacion_actual.autorizacion_incapacidad.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.valor_incapacidad.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.autorizacion_licencia_maternidad.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.valor_licencia_maternidad.iloc[0]
            )

            # cotización arl
            tipo_riesgo = self.liquidacion_actual.clase_riesgo_afiliado.iloc[0]
            porc_riesgo = 0

            if tipo_riesgo == 1:
                porc_riesgo = PORC_ARL_I
            elif tipo_riesgo == 2:
                porc_riesgo = PORC_ARL_II
            elif tipo_riesgo == 3:
                porc_riesgo = PORC_ARL_III
            elif tipo_riesgo == 4:
                porc_riesgo = PORC_ARL_IV
            elif tipo_riesgo == 5:
                porc_riesgo = PORC_ARL_V

            campos_txt.append(
                porc_riesgo
            )
            campos_txt.append(
                self.liquidacion_actual.centro_trabajo.iloc[0]
            )
            campos_txt.append(
                round_100(self.info_ibc_empleado['riesgos'] * porc_riesgo)
            )

            # caja de compensación familiar
            if self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
                campos_txt.append(0)
            else:
                campos_txt.append(
                    PORC_CCF
                )

            campos_txt.append(
                round_100(self.info_ibc_empleado['ccf'] * campos_txt[63])
            )

            # parafiscales
            excepto_parafiscales = True
            if self.info_ibc_empleado['salud'] >= self.info_ibc_empleado.salario_integral:
                excepto_parafiscales = False
            elif self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
                excepto_parafiscales = False

            if excepto_parafiscales or self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
                campos_txt.append(0)
            else:
                campos_txt.append(PORC_SENA)

            campos_txt.append(
                round_100(self.info_ibc_empleado['sena'] * campos_txt[65])
            )

            if excepto_parafiscales or self.info_ibc_empleado.es_practicante_lectivo or self.info_ibc_empleado.es_practicante_productivo:
                campos_txt.append(0)
            else:
                campos_txt.append(PORC_ICBF)

            campos_txt.append(
                round_100(self.info_ibc_empleado['icbf'] * campos_txt[67])
            )

            # valor de novedades - esap
            # se confirma campo en desuso por parte de Sicard - 20/sep
            campos_txt.append(0)
            campos_txt.append(0)

            # valor de novedades - men
            # se confirma campo en desuso por parte de Sicard - 20/sep
            campos_txt.append(0)
            campos_txt.append(0)

            # información adicional
            campos_txt.append(
                self.liquidacion_actual.tipo_doc_cotizante_principal.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.numero_doc_cotizante_principal.iloc[0]
            )

            # excepción de pago eps y parafiscales
            if excepto_parafiscales:
                campos_txt.append('S')
            else:
                campos_txt.append('N')

            # información adicional de riesgos laborales
            campos_txt.append(
                self.liquidacion_actual.cod_arl_pertenece.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.clase_riesgo_afiliado.iloc[0]
            )

            # tarifa especial de pensión
            # se confirma campo no aplica por parte de Sicard - 20/sep
            campos_txt.append('')

            # fechas de novedades
            if self.info_ibc_empleado.status_ingreso:
                campos_txt.append(
                    self.planta_actual.desde.iloc[0].strftime('%Y-%m-%d')
                )
            else:
                campos_txt.append('')

            # retiro aplica desde el día anterior
            if self.info_ibc_empleado.status_retiro:
                campos_txt.append(
                    (self.planta_actual.desde.iloc[0] - DateOffset(days=1)).strftime('%Y-%m-%d')
                )
            else:
                campos_txt.append('')

            if novedad_vsp:
                if self.info_ibc_empleado.status_retiro:
                    campos_txt.append(self.planta_anterior.desde.iloc[0].strftime('%Y-%m-%d'))
                else:
                    campos_txt.append(self.planta_actual.desde.iloc[0].strftime('%Y-%m-%d'))
            else:
                campos_txt.append('')

            campos_txt.append(
                self.liquidacion_actual.fecha_inicio_sln.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_fin_sln.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_inicio_ige.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_fin_ige.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_inicio_lma.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_fin_lma.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_inicio_vac.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_fin_vac.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_inicio_vct.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_inicio_vct.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_inicio_irl.iloc[0]
            )
            campos_txt.append(
                self.liquidacion_actual.fecha_fin_irl.iloc[0]
            )

            # ibc parafiscales
            campos_txt.append(
                self.info_ibc_empleado['sena']
            )

            # horas laboradas
            if INCLUIR_HORAS_DIA:
                campos_txt.append(
                    self.info_ibc_empleado.dias_pagos_salariales * HORAS_POR_DIA
                )
            else:
                campos_txt.append(0)

            # fecha de radicación en el exterior
            campos_txt.append(
                self.liquidacion_actual.fecha_radicacion_exterior.iloc[0]
            )

            # agregar información a la lista principal
            self.info_txt_empleado.append(campos_txt)

        else:
            pass

# -------------------------------------------------------------------
class IBC:
    """Abstrae métodos y atributos requeridos para el IBC"""

    def __init__(self,
                 id_empleado: str,
                 fecha_inicio: pd.Timestamp,
                 fecha_final: pd.Timestamp,
                 nomina_actual: pd.DataFrame = None,
                 nomina_anterior: pd.DataFrame = None,
                 liquidacion_actual: pd.DataFrame = None,
                 planta_actual: pd.DataFrame = None,
                 planta_anterior: pd.DataFrame = None,
                 caso_especial_ibc: bool = False) -> None:
        """
        Inicializa la clase

        Args:
            id_empleado (str):
                ID del empleado
            fecha_inicio (timestamp):
                Fecha de inicio del reporte de liquidación
            fecha_final (timestamp):
                Fecha de finalización del reporte de liquidación
            nomina_actual (dataframe):
                Dataframe pandas con la información de la nómina actual
            nomina_anterior (dataframe):
                Dataframe pandas con la información de la nómina anterior
            liquidacion_actual:
                Dataframe pandas con la liquidación actual
            planta_actual:
                Dataframe pandas con la planta actual
            planta_anterior:
                Dataframe pandas con la planta anterior
            caso_especial_ibc (bool):
                Indica si es un caso especial
                Ya que se requiere calcular parámetros adicionales
        """
        # fechas
        self.fecha_inicio_informe = pd.Timestamp(fecha_inicio)
        self.fecha_fin_informe = pd.Timestamp(fecha_final)

        # dataframe con nómina actual
        self.conceptos_empleados_actual = None
        self.__nomina_actual = nomina_actual

        # dataframe con nómina anterior
        self.__nomina_anterior = nomina_anterior

        self.liquidacion_actual = liquidacion_actual
        self.caso_especial_ibc = caso_especial_ibc
        self.planta_anterior = planta_anterior
        self.planta_actual = planta_actual
        self.id_empleado = id_empleado
        self._ibc = dict()

        self.exoneracion_empresa = EXONERACION_EMPRESA

        # atributos asociados a novedades
        self.__df_pagos_salariales_anterior = pd.DataFrame()
        self.salario_empleado_30_dias_anterior = 0.0
        self.total_pagos_salariales_anterior = 0.0
        self.salario_empleado_anterior = 0.0

        # atributos generales
        self.__df_remuneracion_sin_incapacidades = pd.DataFrame()
        self.__df_remuneracion_sin_vacaciones = pd.DataFrame()
        self.__df_remuneracion_sin_licencias = pd.DataFrame()
        self.__df_remuneracion_sin_auxilios = pd.DataFrame()

        self.__df_pagos_no_salariales = pd.DataFrame()
        self.__df_remuneracion_total = pd.DataFrame()
        self.__df_pagos_salariales = pd.DataFrame()
        self.__df_devengado_total = pd.DataFrame()

        self.total_remuneracion_sin_incapacidades = 0.0
        self.total_remuneracion_sin_vacaciones = 0.0
        self.total_remuneracion_sin_licencias = 0.0
        self.total_remuneracion_sin_auxilios = 0.0
        self.total_pagos_salariales = 0.0
        self.total_remuneracion = 0.0
        self.total_devengado = 0.0

        self.es_variacion_temporal_salario = False
        self.salario_integral_prestacional = 0.0
        self.es_practicante_productivo = False
        self.total_pagos_no_salariales = 0.0
        self.salario_empleado_30_dias = 0.0
        self.es_practicante_lectivo = False
        self.es_pensionado_activo = False
        self.es_salario_integral = True
        self.cotizacion_salarial = 1.0
        self.dias_pagos_salariales = 0
        self.salario_integral = 0.0
        self.salario_empleado = 0.0
        self.status_ingreso = False
        self.status_retiro = False
        self.dias_salario = 0

        self.carga_prestacional_integral = PORCENTAJE_CARGA_PRESTACIONAL_INTEGRAL
        self.n_smmlv_integral = NO_SMMLV_INTEGRAL
        self.smmlv = SMMLV_VALOR

        # manejo pagos no salariales
        self.porc_pagos_no_salariales = PORC_PAGOS_NO_SALARIALES
        self.incluye_pagos_no_salariales = False
        self.valor_ibc_pagos_no_salariales = 0.0
        self.umbral_pagos_no_salariales = 0.0
        self.pagos_no_salariales = 0.0

        # manejo topes
        self._tope_max_salud = TOPE_MAX_SALUD * self.smmlv
        self._tope_min_salud = TOPE_MIN_SALUD * self.smmlv
        self._tope_max_pension = TOPE_MAX_PENSION * self.smmlv
        self._tope_min_pension = TOPE_MIN_PENSION * self.smmlv
        self._tope_max_riesgos = TOPE_MAX_RIESGOS * self.smmlv
        self._tope_min_riesgos = TOPE_MIN_RIESGOS * self.smmlv

        # ajuste dataframe
        self._resumen = self.__nomina_actual.loc[
            :, ['cod_concepto', 'nota', 'cantidad', 'importe']
        ]
        self._resumen = self._resumen.rename(columns={
            'cantidad': 'cant_concepto', 'importe': 'valor_concepto'
        })
        self._resumen.nota = self._resumen.nota.str.strip().str.lower()

        self.conceptos_empleados_actual = self._resumen.cod_concepto.unique().tolist()

        if isinstance(self.__nomina_anterior, pd.DataFrame):
            self._resumen_anterior = self.__nomina_anterior.loc[
                :, ['cod_concepto', 'nota', 'cantidad', 'importe']
            ]
            self._resumen_anterior = self._resumen_anterior.rename(columns={
                'cantidad': 'cant_concepto', 'importe': 'valor_concepto'
            })
            self._resumen_anterior.nota = self._resumen_anterior.nota.str.strip().str.lower()

        # ejecución de funciones iniciales
        self.__calcular_parametros()

        self.__pagos_no_salariales()
        self._ibc_parafiscales()
        self._ibc_salud()
        self._ibc_pension()
        self._ibc_riesgos()

    # ---------------------------------------------------------------
    def __str__(self) -> str:
        """
        Genera un string que resumen la información de la clase

        Return:
            Cadena de texto
        """
        info_tmp = '''

        -------------------------------------------------
        EMPLEADO: {}
        -------------------------------------------------

        Se considera caso especial: {}

        Salario empleado: ${:,.2f} (30 días)
        Salario empleado: ${:,.2f} ({:.0f} días)

        Total pagos salariales: ${:,.2f}
        Total remuneración: ${:,.2f}
        Total devengado: ${:,.2f}

        Pagos no salariales: ${:,.2f}
        Se incluyen % pagos no salariales: {}

        IBC:
            - Salud: ${:,.2f}
            - Pensión: ${:,.2f}
            - ARL: ${:,.2f}
            - CCF: ${:,.2f}
            - ICBF: ${:,.2f}
            - SENA: ${:,.2f}

        '''.format(
            self.id_empleado,
            self.caso_especial_ibc,
            self.salario_empleado_30_dias,
            self.salario_empleado,
            self.dias_salario,
            self.total_pagos_salariales,
            self.total_remuneracion,
            self.total_devengado,
            self.total_pagos_no_salariales,
            self.incluye_pagos_no_salariales,
            self._ibc.get('salud'),
            self._ibc.get('pension'),
            self._ibc.get('riesgos'),
            self._ibc.get('ccf'),
            self._ibc.get('icbf'),
            self._ibc.get('sena')
        )

        return info_tmp

    # ---------------------------------------------------------------
    def __getitem__(self, tipo_ibc: str) -> float:
        """
        Recuperar el valor de un IBC en particular

        Args:
            tipo_ibc (str):
                Nombre del IBC:
                salud, pension, arl, parafiscales
        """
        if self._ibc:
            return self._ibc.get(tipo_ibc, None)
        else:
            return

    # ---------------------------------------------------------------
    def __calcular_parametros(self) -> None:
        """
        Cálcula los parámetros requeridos para el IBC
        """
        # verificación de practicante
        if self.liquidacion_actual.tipo_cotizante.iloc[0] == 12:
            self.es_practicante_lectivo = True
        elif self.liquidacion_actual.tipo_cotizante.iloc[0] == 19:
            self.es_practicante_productivo = True

        # verificación de pensionado
        if self.liquidacion_actual.subtipo_cotizante.iloc[0] == 1:
            self.es_pensionado_activo = True

        # verificación de variación transitoria de salario
        if self.liquidacion_actual.variacion_transitoria_salario.iloc[0] == 'X':
            self.es_variacion_temporal_salario = True

         # determinar si es salario integral
        tmp_check_salario_int = self.liquidacion_actual[
            self.liquidacion_actual.no_personal == self.id_empleado
        ]
        if tmp_check_salario_int.iloc[0,:].tipo_salario == 'X':
            self.cotizacion_salarial = COTIZACION_SALARIO_INTEGRAL

        # dataframes
        tmp = self._resumen.copy()

        # casos especiales
        if self.caso_especial_ibc:
            tmp_anterior = self._resumen.copy()

            self.__df_pagos_salariales_anterior = tmp[
                tmp_anterior.nota.str.contains('^salarial|^soste', na=False, regex=True)
            ].copy()

            try:
                self.salario_empleado_30_dias_anterior = self.planta_anterior.importe.iloc[0]
            except IndexError:
                self.salario_empleado_30_dias_anterior = 0

            self.__df_remuneracion_sin_vacaciones = tmp[
                ~tmp.cod_concepto.isin(CONCEPTOS_VACACIONES)
            ].copy()

            self.__df_remuneracion_sin_auxilios = tmp[
                ~tmp.cod_concepto.isin(CONCEPTOS_AUXILIOS)
            ].copy()

            self.__df_remuneracion_sin_incapacidades = tmp[
                ~tmp.cod_concepto.isin(CONCEPTOS_INCAPACIDADES)
            ].copy()

            self.__df_remuneracion_sin_licencias = tmp[
                ~tmp.cod_concepto.isin(CONCEPTOS_LICENCIAS)
            ].copy()

            self.total_pagos_salariales_anterior = self.__df_pagos_salariales_anterior.valor_concepto.sum()
            self.total_remuneracion_sin_incapacidades = self.__df_remuneracion_sin_incapacidades.valor_concepto.sum()
            self.total_remuneracion_sin_vacaciones = self.__df_remuneracion_sin_vacaciones.valor_concepto.sum()
            self.total_remuneracion_sin_licencias = self.__df_remuneracion_sin_licencias.valor_concepto.sum()
            self.total_remuneracion_sin_auxilios = self.__df_remuneracion_sin_auxilios.valor_concepto.sum()

        # remuneración
        self.__df_remuneracion_total = tmp[
            tmp.nota.str.contains('salarial', na=False, regex=True)
        ].copy()

        # devengado
        self.__df_devengado_total = tmp[
            tmp.nota.str.contains('salarial|vacaciones|soste', na=False, regex=True)
        ].copy()

        # pagos salariales
        self.__df_pagos_salariales = tmp[
            tmp.nota.str.contains('^salarial|^soste', na=False, regex=True)
        ].copy()

        self.total_pagos_salariales = self.__df_pagos_salariales.valor_concepto.sum()
        self.total_remuneracion = self.__df_remuneracion_total.valor_concepto.sum()
        self.total_devengado = self.__df_devengado_total.valor_concepto.sum()

        # pagos no salariales
        self.__df_pagos_no_salariales = tmp[
            tmp.nota.str.contains('no salarial', na=False, regex=True)
        ].copy()

        self.total_pagos_no_salariales = self.__df_pagos_no_salariales.valor_concepto.sum()

        # cálculo de días
        self.dias_salario = float(tmp[
            tmp.cod_concepto.isin(CONCEPTOS_INGRESOS_EMPLEADOS)
        ]['cant_concepto'].sum())
        self.dias_pagos_salariales = self.__df_pagos_salariales.cant_concepto.sum()

        # ibc caja de compensación familiar
        if self.es_practicante_lectivo or self.es_practicante_productivo:
            self._ibc['ccf'] = 0

            # salario 30 días
            self.salario_empleado_30_dias = SMMLV_VALOR

        else:
            valor_ibc_mes_ccf = self.total_pagos_salariales * self.cotizacion_salarial
            self._ibc['ccf'] = self.__valor_proporcional(
                valor_ibc_mes_ccf, self.dias_pagos_salariales
            )
            # salario 30 días
            self.salario_empleado_30_dias = self.planta_actual.importe.iloc[0]

        self.salario_empleado = float(tmp[
            tmp.cod_concepto.isin(CONCEPTOS_INGRESOS_EMPLEADOS)
        ]['valor_concepto'].sum())

        # umbral para los parafiscales
        # ley 50/1990 - art. 132 cst
        self.salario_integral_prestacional = (self.n_smmlv_integral * self.smmlv) * (1 + self.carga_prestacional_integral)
        self.salario_integral = (self.n_smmlv_integral * self.smmlv)

        # revisión de ingreso y retiro
        aplica_novedad_cr = False
        fecha_novedad_cr = self.planta_actual.desde.iloc[0]

        if fecha_novedad_cr.year >= self.fecha_inicio_informe.year and fecha_novedad_cr.month >= self.fecha_fin_informe.month:
            aplica_novedad_cr = True

        if self.planta_actual.clase.iloc[0] == 'Contratación' and aplica_novedad_cr:
            self.status_ingreso = True

        if self.planta_actual.clase.iloc[0] == 'Baja' and aplica_novedad_cr:
            self.status_retiro = True

    # ---------------------------------------------------------------
    def __pagos_no_salariales(self) -> None:
        """
        Calcula los pagos no salariales del empleados y asigna
        los valores correspondientes a las atributos de la clase
        """
        # umbral para los pagos no salariales
        # art. 30 1393/2010
        self.umbral_pagos_no_salariales = self.total_remuneracion * self.porc_pagos_no_salariales
        # diferencia
        diff_remuneracion_pns = self.total_pagos_no_salariales - self.umbral_pagos_no_salariales

        # condición para incluir pagos no salariales
        if diff_remuneracion_pns > 0:
            self.valor_ibc_pagos_no_salariales = diff_remuneracion_pns
            self.incluye_pagos_no_salariales = True

    # ---------------------------------------------------------------
    def _ibc_parafiscales(self) -> None:
        """
        Calcula el IBC para el componente de parafiscales
        """
        # casos especiales - salario anterior anterior
        if self.caso_especial_ibc:
            valor_ibc_mes = (self.salario_empleado_30_dias_anterior + self.total_pagos_salariales) * self.cotizacion_salarial
        else:
            valor_ibc_mes = self.total_pagos_salariales * self.cotizacion_salarial

        # condición para incluir el pago de parafiscales
        if self.total_pagos_salariales > self.salario_integral:
            # cálculo proporcional
            self._ibc['icbf'] = self.__valor_proporcional(
                valor_ibc_mes, self.dias_pagos_salariales
            )
            self._ibc['sena'] = self.__valor_proporcional(
                valor_ibc_mes, self.dias_pagos_salariales
            )

        else:
            if self.exoneracion_empresa or self.es_practicante_lectivo or self.es_practicante_productivo:
                self._ibc['icbf'] = 0.0
                self._ibc['sena'] = 0.0

            else:
                self._ibc['icbf'] = self.__valor_proporcional(
                    valor_ibc_mes, self.dias_pagos_salariales
                )
                self._ibc['sena'] = self.__valor_proporcional(
                    valor_ibc_mes, self.dias_pagos_salariales
                )

    # ---------------------------------------------------------------
    def _ibc_salud(self) -> None:
        """
        Calcula el IBC para el componente de salud
        """
        if self.incluye_pagos_no_salariales:
            tmp = self.total_remuneracion + self.valor_ibc_pagos_no_salariales

        elif self.es_practicante_lectivo or self.es_practicante_productivo:
            tmp = SMMLV_VALOR

        # casos especiales - salario anterior anterior
        elif self.caso_especial_ibc:
            tmp = self.salario_empleado_30_dias_anterior + self.total_pagos_salariales

        else:
            tmp = self.total_pagos_salariales

        tmp = tmp * self.cotizacion_salarial

        if self.status_retiro or self.status_ingreso or self.es_practicante_lectivo or self.es_practicante_productivo:
            valor_ibc_mes = tmp

        else:
            valor_ibc_mes = self.__aplicar_tope(tmp, 'salud')

        # cálculo proporcional
        self._ibc['salud'] = self.__valor_proporcional(
            valor_ibc_mes, self.dias_pagos_salariales
        )

    # ---------------------------------------------------------------
    def _ibc_pension(self) -> None:
        """
        Calcula el IBC para el componente de salud
        """
        if self.incluye_pagos_no_salariales:
            tmp = self.total_remuneracion + self.valor_ibc_pagos_no_salariales

        # contrato de aprendizaje no es un contrato laboral
        elif self.es_practicante_lectivo or self.es_practicante_productivo:
            tmp = 0

        # casos especiales - salario anterior anterior
        elif self.caso_especial_ibc:
            tmp = self.salario_empleado_30_dias_anterior

        else:
            tmp = self.total_pagos_salariales

        tmp = tmp * self.cotizacion_salarial

        if self.status_retiro or self.status_ingreso or self.es_practicante_lectivo or self.es_practicante_productivo:
            valor_ibc_mes = tmp

        else:
            valor_ibc_mes = self.__aplicar_tope(tmp, 'pension')

        # cálculo proporcional
        self._ibc['pension'] = self.__valor_proporcional(
            valor_ibc_mes, self.dias_pagos_salariales
        )

    # ---------------------------------------------------------------
    def _ibc_riesgos(self) -> None:
        """
        Calcula el IBC para el componente de salud
        """
        if self.incluye_pagos_no_salariales:
            tmp = self.total_remuneracion_sin_vacaciones + self.valor_ibc_pagos_no_salariales

        # solo el practicante en etapa productiva es quien requiere arl
        elif self.es_practicante_productivo:
            tmp = SMMLV_VALOR

        # aprendices en etapa lectiva no están expuestos a riesgos laborales
        # art. 2.2.6.3.5 dec. 1072/2015
        elif self.es_practicante_lectivo:
            tmp = 0

        # casos especiales - salario anterior anterior
        elif self.caso_especial_ibc:
            tmp = self.salario_empleado_30_dias_anterior + self.total_pagos_salariales

        else:
            tmp = self.total_pagos_salariales

        tmp = tmp * self.cotizacion_salarial

        if self.status_retiro or self.status_ingreso or self.es_practicante_lectivo or self.es_practicante_productivo:
            valor_ibc_mes = tmp

        else:
            valor_ibc_mes = self.__aplicar_tope(tmp, 'riesgos')

        # cálculo proporcional
        self._ibc['riesgos'] = self.__valor_proporcional(
            valor_ibc_mes, self.dias_pagos_salariales
        )

    # ---------------------------------------------------------------
    def __valor_proporcional(self,
                             valor_ibc: Union[int, float],
                             dias: int,
                             total: int = 30,
                             redondear: bool = True) -> int:
        """
        Calcula el valor proporcional de un IBC

        Args:
            valor_ibc (int, float):
                Valor IBC 30 días
            dias (int):
                Días proporcionales
            total (int):
                Total de días mes
            redondear (int):
                Indica si se debe redondear el resultado

        Return:
            Valor entero
        """
        if not isinstance(valor_ibc, (int, float)):
            valor_ibc = 0

        if total <= 0:
            total = 30

        ibc_dia = Decimal(valor_ibc) / total
        dias = Decimal(dias)

        if redondear:
            return ceil(ibc_dia * dias)
        else:
            return ibc_dia * dias

    # ---------------------------------------------------------------
    def __aplicar_tope(self,
                       valor_ibc: Union[int, float],
                       type_ibc: str) -> int:
        """
        Calcula el valor proporcional de un IBC

        Args:
            valor_ibc (int, float):
                Valor del IBC estimado
            type_ibc (int):
                Tipo de IBC

        Return:
            Valor entero
        """
        if type_ibc == 'salud':
            tope_max = self._tope_max_salud
            tope_min = self._tope_min_salud

        elif type_ibc == 'pension':
            tope_max = self._tope_max_pension
            tope_min = self._tope_min_pension

        else:
            tope_max = self._tope_max_riesgos
            tope_min = self._tope_min_riesgos

        tmp = min(valor_ibc, tope_max)

        return max(tmp, tope_min)


# -------------------------------------------------------------------
class Data():
    """Permite convertir queries de Django en objetos de pandas"""

    ALLOWED_MODELS = ('Empresa', 'Planta', 'Nomina', 'Liquidacion')

    def __init__(self,
                 modelo: str,
                 fecha_inicio: str = None,
                 fecha_fin: str = None,
                 campos_requeridos: list = None,
                 actual: bool = True,
                 **kwargs) -> None:
        """
        Inicializa la clase

        Args:
            modelo (str):
                Nombre del modelo
            fecha_inicio (str):
                Fecha de inicio de los datos del modelo
            fecha_fin (str):
                Fecha de finalización de los datos del modelo
            campos_requeridos (list):
                Contiene los campos que se requieren consultar, si
                es None extrae todos los campos
            actual (bool):
                Indica si se trata del archivo actual en caso de ser
                True y el anterior si es False
            **kwargs:
                Ruta para leer localmente los archivos del modelo,
                de la forma: Modelo=Ruta
        """
        self.campos_requeridos = campos_requeridos
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.actual = actual
        self.kwargs = kwargs

        self.__modelo = None
        self.__df = None

        self.modelo = modelo

    # ---------------------------------------------------------------
    @property
    def modelo(self) -> str:
        """
        Retorna el nombre del modelo asociado a la clase

        Return:
            String con el nombre del modelo
        """
        return self.__modelo

    # ---------------------------------------------------------------
    @modelo.setter
    def modelo(self, value: str) -> None:
        """
        Verifica y asigna el valor del modelo a un atributo de la clase

        Args:
            value (str):
                Nombre del modelo
        """
        if not isinstance(value, str):
            raise InvalidParameterModel('modelo', 'string')

        if value in self.ALLOWED_MODELS:
            self.__modelo = value

        else:
            raise ValueIncorrectModel('modelo',
                                      'ser ' + ', '.join(self.ALLOWED_MODELS))

    # ---------------------------------------------------------------
    @property
    def df(self) -> pd.DataFrame:
        """
        Retorna el dataframe pandas resultante de la conversión
        de las queries de Django

        Return:
            Dataframe pandas
        """
        # si ya existe el dataframe lo retorna
        if isinstance(self.__df, pd.DataFrame):
            return self.__df

        # si no existe aún, lo genera
        else:
            if self.modelo == 'Empresa':
                self.__obtener_empresa()

            elif self.modelo == 'Planta':
                self.__obtener_planta()

            elif self.modelo == 'Nomina':
                self.__obtener_nomina()

            elif self.modelo == 'Liquidacion':
                self.__obtener_liquidacion()

            return self.__df

    # ---------------------------------------------------------------
    def __obtener_nomina(self) -> pd.DataFrame:
        """
        Obtiene los datos de nómina correspondiente

        Return:
            Dataframe pandas
        """
        if 'Nomina_actual' in self.kwargs.keys() and self.actual:
            data = leer_datos_archivo(self.kwargs['Nomina_actual'])

        elif 'Nomina_anterior' in self.kwargs.keys() and not self.actual:
            data = leer_datos_archivo(self.kwargs['Nomina_anterior'])

        else:
            data_django = Nomina.objects.filter( # noqa
                id_empresa = self.empresa,
                fecha_inicia = [self.fecha_inicio, self.fecha_fin]
            )

            data = pd.DataFrame(
                list(data_django.values)
            )

        # busca campos requeridos
        if isinstance(self.campos_requeridos, list):
            if len(self.campos_requeridos) > 0:
                check_campos = []
                columnas = data.columns.tolist()

                for campo in self.campos_requeridos:
                    if campo in columnas:
                        check_campos.append(campo)

                data = data[check_campos]

        self.__df = data.fillna('')

    # ---------------------------------------------------------------
    def __obtener_planta(self) -> pd.DataFrame:
        """
        Obtiene los datos de la planta correspondiente

        Return:
            Dataframe pandas
        """
        if 'Planta_actual' in self.kwargs.keys() and self.actual:
            data = leer_datos_archivo(self.kwargs['Planta_actual'])
            data.fecha = pd.to_datetime(data.fecha, format='%m/%d/%Y')
            data.desde = pd.to_datetime(data.desde, format='%m/%d/%Y')

        elif 'Planta_anterior' in self.kwargs.keys() and not self.actual:
            data = leer_datos_archivo(self.kwargs['Planta_anterior'])
            data.fecha = pd.to_datetime(data.fecha, format='%m/%d/%Y')
            data.desde = pd.to_datetime(data.desde, format='%m/%d/%Y')

        else:
            data_django = Planta.objects.filter( # noqa
                id_empresa = self.empresa,
                fecha_inicia = [self.fecha_inicio, self.fecha_fin]
            )

            data = pd.DataFrame(
                list(data_django.values)
            )

        # busca campos requeridos
        if isinstance(self.campos_requeridos, list):
            if len(self.campos_requeridos) > 0:
                check_campos = []
                columnas = data.columns.tolist()

                for campo in self.campos_requeridos:
                    if campo in columnas:
                        check_campos.append(campo)

                data = data[check_campos]

        self.__df = data.fillna('')

    # ---------------------------------------------------------------
    def __obtener_liquidacion(self) -> pd.DataFrame:
        """
        Obtiene los datos de la liquidación

        Return:
            Dataframe pandas
        """
        if 'Liquidacion_actual' in self.kwargs.keys() and self.actual:
            data = leer_datos_archivo(self.kwargs['Liquidacion_actual'])

        elif 'Liquidacion_anterior' in self.kwargs.keys() and not self.actual:
            data = leer_datos_archivo(self.kwargs['Liquidacion_anterior'])

        else:
            data_django = Liquidacion.objects.filter(
                id_empresa = self.empresa,
                fecha_inicia = [self.fecha_inicio, self.fecha_fin]
            )

            data = pd.DataFrame(
                list(data_django.values)
            )

        if isinstance(self.campos_requeridos, list):
            if len(self.campos_requeridos) > 0:
                check_campos = []
                columnas = data.columns.tolist()

                for campo in self.campos_requeridos:
                    if campo in columnas:
                        check_campos.append(campo)

                data = data[check_campos]

        self.__df = data.fillna('')

    # ---------------------------------------------------------------
    def __obtener_empresa(self) -> pd.DataFrame:
        """
        Obtiene los datos de la empresa

        Return:
            Dataframe pandas
        """
        if 'Empresa' in self.kwargs:
            data = leer_datos_archivo(self.kwargs['Empresa'])

        else:
            data_django = Empresa.objects.filter(
                id_empresa = self.empresa
            )

            data = pd.DataFrame(
                list(data_django.values)
            )

        if isinstance(self.campos_requeridos, list):
            if len(self.campos_requeridos) > 0:
                check_campos = []
                columnas = data.columns.tolist()

                for campo in self.campos_requeridos:
                    if campo in columnas:
                        check_campos.append(campo)

                data = data[check_campos]

        self.__df = data
