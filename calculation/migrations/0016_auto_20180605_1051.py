# Generated by Django 2.0.5 on 2018-06-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0015_auto_20180605_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regprice',
            name='created_at',
            field=models.DateField(db_index=True, verbose_name='создано'),
        ),
    ]
