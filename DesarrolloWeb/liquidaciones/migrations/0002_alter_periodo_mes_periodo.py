# Generated by Django 3.2.15 on 2022-09-22 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liquidaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='mes_periodo',
            field=models.CharField(choices=[('01', 1), ('02', 2), ('03', 3), ('04', 4), ('05', 5), ('06', 6), ('07', 7), ('08', 8), ('09', 9), ('10', 10), ('11', 11), ('12', 12)], max_length=3),
        ),
    ]