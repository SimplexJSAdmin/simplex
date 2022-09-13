# Generated by Django 3.2.15 on 2022-09-02 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ARL',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cod_miplanilla', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ConceptoInterno',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('desc_concepto', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id_empresa', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_empresa', models.CharField(max_length=75, verbose_name='Nombre de la empresa')),
            ],
        ),
        migrations.CreateModel(
            name='EPS',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cod_miplanilla', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FondoPension',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cod_miplanilla', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Globales',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_global', models.CharField(max_length=75)),
                ('valor', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id_periodo', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Topes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tope', models.CharField(max_length=75)),
                ('clasificacion', models.CharField(max_length=100)),
                ('limite_superior', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('no_personal', models.IntegerField()),
                ('primer_apellido', models.CharField(default='', max_length=75)),
                ('segundo_apellido', models.CharField(default='', max_length=75)),
                ('primer_nombre', models.CharField(default='', max_length=75)),
                ('segundo_nombre', models.CharField(default='', max_length=75)),
                ('tipo_documento', models.CharField(default='', max_length=75)),
                ('documento', models.CharField(default='', max_length=75, primary_key=True, serialize=False)),
                ('division_persona', models.CharField(default='', max_length=75)),
                ('denominacion_funcion', models.CharField(default='', max_length=75)),
                ('und_tiempo_nomina', models.CharField(default='', max_length=75)),
                ('cc', models.CharField(default='', max_length=75)),
                ('cuenta_bancaria', models.CharField(default='', max_length=75)),
                ('clase_contrato', models.CharField(default='', max_length=75)),
                ('procedimiento_retencion', models.CharField(default='', max_length=75)),
                ('porcentaje_retencion', models.FloatField()),
                ('declarante_renta', models.CharField(default='', max_length=75)),
                ('tiene_independientes', models.CharField(default='', max_length=75)),
                ('importe', models.FloatField()),
                ('moneda', models.CharField(default='', max_length=75)),
                ('texto_breve', models.CharField(default='', max_length=75)),
                ('correo_electronico', models.CharField(default='', max_length=75)),
                ('centro_coste', models.CharField(default='', max_length=75)),
                ('fecha', models.DateField()),
                ('grupo_personal', models.CharField(default='', max_length=75)),
                ('clase', models.CharField(default='', max_length=75)),
                ('desde', models.DateField(default='')),
                ('denominacion_posicion', models.CharField(default='', max_length=75)),
                ('denominacion_medicion', models.CharField(default='', max_length=75)),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquidaciones.empresa')),
                ('id_periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquidaciones.periodo')),
            ],
        ),
        migrations.CreateModel(
            name='Nomina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_personal', models.IntegerField()),
                ('apellido_nombre', models.CharField(max_length=75)),
                ('nombre_completo', models.CharField(max_length=75)),
                ('NIF', models.CharField(max_length=75)),
                ('divp', models.CharField(max_length=75)),
                ('division_persona', models.CharField(max_length=75)),
                ('percalnom', models.CharField(max_length=75)),
                ('area_nomina', models.CharField(max_length=75)),
                ('paper', models.CharField(max_length=75)),
                ('denom_periodos', models.CharField(max_length=75)),
                ('periodo_inicia', models.IntegerField()),
                ('fecha_inicia', models.DateField()),
                ('tpclcnom', models.CharField(max_length=75)),
                ('idnom', models.CharField(max_length=75)),
                ('area_cal_nom', models.CharField(max_length=75)),
                ('area_nomina2', models.CharField(max_length=75)),
                ('paper2', models.CharField(max_length=75)),
                ('denom_periodos2', models.CharField(max_length=75)),
                ('periodo_fin', models.IntegerField()),
                ('fecha_fin', models.DateField()),
                ('tpclcnom2', models.CharField(max_length=75)),
                ('idnom2', models.CharField(max_length=75)),
                ('ag_pai', models.CharField(max_length=75)),
                ('desc_concepto', models.CharField(max_length=150)),
                ('cantidad', models.IntegerField()),
                ('importe', models.FloatField()),
                ('moneda', models.CharField(max_length=75)),
                ('cod_concepto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquidaciones.conceptointerno')),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquidaciones.empresa')),
                ('id_periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquidaciones.periodo')),
            ],
        ),
        migrations.CreateModel(
            name='Liquidaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_liquidacion', models.CharField(default='', max_length=15)),
                ('radicado_liquidacion', models.CharField(default='', max_length=30)),
                ('fecha_radicado_liquidacion', models.DateField()),
                ('tipo_registro', models.CharField(default='02', max_length=2)),
                ('secuencia', models.CharField(default='', max_length=5)),
                ('tipo_doc_cotizante', models.CharField(default='', max_length=2)),
                ('num_doc_cotizante', models.CharField(default='', max_length=16)),
                ('tipo_cotizante', models.CharField(default='', max_length=2)),
                ('subtipo_cotizante', models.CharField(default='', max_length=2)),
                ('extranjero', models.CharField(default='', max_length=1)),
                ('colombian_en_exterior', models.CharField(default='', max_length=1)),
                ('cod_departamento', models.CharField(default='', max_length=2)),
                ('cod_municipio', models.CharField(default='', max_length=3)),
                ('primer_apellido', models.CharField(default='', max_length=20)),
                ('segundo_apellido', models.CharField(default='', max_length=30)),
                ('primer_nombre', models.CharField(default='', max_length=20)),
                ('segundo_nombre', models.CharField(default='', max_length=30)),
                ('ingreso', models.CharField(default='', max_length=1)),
                ('retiro', models.CharField(default='', max_length=1)),
                ('traslado_desde_eps', models.CharField(default='', max_length=1)),
                ('traslado_hacia_eps', models.CharField(default='', max_length=1)),
                ('traslado_desde_fondo_pension', models.CharField(default='', max_length=1)),
                ('traslado_hacia_fondo_pension', models.CharField(default='', max_length=1)),
                ('variacion_permanente_salario', models.CharField(default='', max_length=1)),
                ('correcion', models.CharField(default='', max_length=1)),
                ('variacion_transitoria_salario', models.CharField(default='', max_length=1)),
                ('suspencion_temporal', models.CharField(default='', max_length=1)),
                ('incapacidad_temporal', models.CharField(default='', max_length=1)),
                ('licencia_maternidad_paternidad', models.CharField(default='', max_length=1)),
                ('vacaciones_licencia_remunerada', models.CharField(default='', max_length=1)),
                ('aporte_voluntario', models.CharField(default='', max_length=1)),
                ('variacion_centros_trabajo', models.CharField(default='', max_length=1)),
                ('dias_incapacidad', models.CharField(default='', max_length=2)),
                ('cod_fondo_pension_pertence', models.CharField(default='', max_length=6)),
                ('cod_fondo_pension_tralasda', models.CharField(default='', max_length=6)),
                ('cod_eps_pertenece', models.CharField(default='', max_length=6)),
                ('cod_eps_tralasda', models.CharField(default='', max_length=6)),
                ('cod_ccf_pertenece', models.CharField(default='', max_length=6)),
                ('dias_fondo_pension', models.CharField(default='', max_length=2)),
                ('dias_eps', models.CharField(default='', max_length=2)),
                ('dias_arl', models.CharField(default='', max_length=2)),
                ('dias_ccf', models.CharField(default='', max_length=2)),
                ('salario_basico', models.CharField(default='', max_length=9)),
                ('tipo_salario', models.CharField(default='', max_length=1)),
                ('ibc_fondo_pension', models.CharField(default='', max_length=9)),
                ('ibc_eps', models.CharField(default='', max_length=9)),
                ('ibc_arl', models.CharField(default='', max_length=9)),
                ('ibc_ccf', models.CharField(default='', max_length=9)),
                ('tarifa_fondo_pension', models.CharField(default='', max_length=7)),
                ('cotizacion_obligatoria_pension', models.CharField(default='', max_length=9)),
                ('aporte_voluntario_afiliado_pension', models.CharField(default='', max_length=9)),
                ('aporte_voluntario_aportante_pension', models.CharField(default='', max_length=9)),
                ('tota_cotizacion_pension', models.CharField(default='', max_length=9)),
                ('aporte_fondo_solidaridad', models.CharField(default='', max_length=9)),
                ('aporte_fondo_subsistencia', models.CharField(default='', max_length=9)),
                ('valor_no_retenido', models.CharField(default='', max_length=9)),
                ('tarifa_eps', models.CharField(default='', max_length=7)),
                ('cotizacion_obligatoria_eps', models.CharField(default='', max_length=9)),
                ('ups_adres', models.CharField(default='', max_length=9)),
                ('autorizacion_incapacidad', models.CharField(default='', max_length=15)),
                ('valor_incapacidad', models.CharField(default='', max_length=9)),
                ('autorizacion_licencia_maternidad', models.CharField(default='', max_length=15)),
                ('valor_licencia_maternidad', models.CharField(default='', max_length=9)),
                ('tarifa_arl', models.CharField(default='', max_length=9)),
                ('centro_trabajo', models.CharField(default='', max_length=9)),
                ('cotizacion_obligatoria_arl', models.CharField(default='', max_length=9)),
                ('tarifa_ccf', models.CharField(default='', max_length=7)),
                ('valor_aporte_ccf', models.CharField(default='', max_length=9)),
                ('tarifa_sena', models.CharField(default='', max_length=7)),
                ('valor_aporte_sena', models.CharField(default='', max_length=9)),
                ('tarifa_icbf', models.CharField(default='', max_length=7)),
                ('valor_aporte_icbf', models.CharField(default='', max_length=9)),
                ('tarifa_esap', models.CharField(default='', max_length=7)),
                ('valor_aporte_esap', models.CharField(default='', max_length=9)),
                ('tarifa_men', models.CharField(default='', max_length=7)),
                ('valor_aporte_men', models.CharField(default='', max_length=9)),
                ('tipo_doc_cotizante_principal', models.CharField(default='', max_length=2)),
                ('numero_doc_cotizante_principal', models.CharField(default='', max_length=16)),
                ('exonerado_pago_eps_sena_icbf', models.CharField(default='', max_length=1)),
                ('cod_arl_pertenece', models.CharField(default='', max_length=6)),
                ('clase_riesgo_afiliado', models.CharField(default='', max_length=1)),
                ('indicador_tarifa_especial_pension', models.CharField(default='', max_length=1)),
                ('fecha_ingreso', models.CharField(default='', max_length=10)),
                ('fecha_retiro', models.CharField(default='', max_length=10)),
                ('fecha_inicio_vsp', models.CharField(default='', max_length=10)),
                ('fecha_inicio_sln', models.CharField(default='', max_length=10)),
                ('fecha_fin_sln', models.CharField(default='', max_length=10)),
                ('fecha_inicio_ige', models.CharField(default='', max_length=10)),
                ('fecha_fin_ige', models.CharField(default='', max_length=10)),
                ('fecha_inicio_lma', models.CharField(default='', max_length=10)),
                ('fecha_fin_lma', models.CharField(default='', max_length=10)),
                ('fecha_inicio_vac', models.CharField(default='', max_length=10)),
                ('fecha_fin_vac', models.CharField(default='', max_length=10)),
                ('fecha_inicio_vct', models.CharField(default='', max_length=10)),
                ('fecha_inicio_irl', models.CharField(default='', max_length=10)),
                ('fecha_fin_irl', models.CharField(default='', max_length=10)),
                ('ibc_otros_parafiscales', models.CharField(default='', max_length=9)),
                ('numero_horas_laboradas', models.CharField(default='', max_length=3)),
                ('fecha_radicacion_exterior', models.CharField(default='', max_length=10)),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquidaciones.empresa')),
                ('id_periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquidaciones.periodo')),
            ],
        ),
        migrations.CreateModel(
            name='ConceptoEmmpresa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('desc_concepto', models.CharField(max_length=150)),
                ('id_concepto_interno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquidaciones.conceptointerno')),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquidaciones.empresa')),
            ],
        ),
    ]