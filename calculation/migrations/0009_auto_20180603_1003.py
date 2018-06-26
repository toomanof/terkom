# Generated by Django 2.0.5 on 2018-06-03 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0008_auto_20180602_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='out',
            field=models.PositiveIntegerField(blank=True, db_index=True, editable=False, null=True, verbose_name='выход'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='tech_map',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dish', to='calculation.Map', verbose_name='технологическая карта'),
        ),
    ]
