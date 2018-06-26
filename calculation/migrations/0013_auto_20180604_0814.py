# Generated by Django 2.0.5 on 2018-06-04 08:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0012_auto_20180604_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='dish',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, related_name='menu_dish', to='calculation.Dish', verbose_name='блюдо'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='food_intake',
            field=models.PositiveIntegerField(choices=[(1, 'Завтрак'), (2, 'Обед'), (3, 'Полдник'), (4, '1-й ужин'), (5, '2-й ужин')], db_index=True, verbose_name='приём пищи'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='out',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='выход порции'),
        ),
    ]
