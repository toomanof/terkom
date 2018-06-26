# Generated by Django 2.0.5 on 2018-06-02 18:30

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0007_auto_20180602_1742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='map',
            options={'ordering': ['name'], 'verbose_name': 'Технологическая карта', 'verbose_name_plural': 'Технологические карты'},
        ),
        migrations.RemoveField(
            model_name='map',
            name='number',
        ),
        migrations.AddField(
            model_name='map',
            name='batch_output',
            field=models.CharField(blank=True, max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='выход порции'),
        ),
        migrations.AlterField(
            model_name='map',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='создано'),
        ),
    ]
