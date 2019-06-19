# Generated by Django 2.0.5 on 2019-06-19 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0049_auto_20190502_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapitems',
            name='brutto',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='брутто'),
        ),
        migrations.AlterField(
            model_name='mapitems',
            name='netto',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=15, null=True, verbose_name='неттто'),
        ),
    ]
