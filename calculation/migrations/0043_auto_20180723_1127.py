# Generated by Django 2.0.5 on 2018-07-23 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0042_registration_dish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='dish',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='calculation.Dish', verbose_name='блюдо'),
        ),
    ]
