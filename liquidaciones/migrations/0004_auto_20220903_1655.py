# Generated by Django 3.2.15 on 2022-09-03 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liquidaciones', '0003_empresaspermitidas'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ConceptoEmmpresa',
            new_name='ConceptoEmpresa',
        ),
        migrations.AddField(
            model_name='conceptointerno',
            name='tipo_concepto',
            field=models.CharField(choices=[('salarial', 'Salarial'), ('no_salarial', 'No salarial')], default='salarial', max_length=12),
        ),
    ]