# Generated by Django 2.0.5 on 2018-06-25 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0029_auto_20180621_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='вес в килограммах                                                 одной единицы'),
        ),
    ]
