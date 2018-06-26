# Generated by Django 2.0.5 on 2018-06-18 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0025_auto_20180615_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='motion',
            field=models.SmallIntegerField(choices=[(1, 'приход'), (0, 'расход')], default=1),
        ),
        migrations.AlterField(
            model_name='registration',
            name='motion',
            field=models.SmallIntegerField(choices=[(1, 'приход'), (0, 'расход')], default=1),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together={('created_at', 'food_intake', 'dish')},
        ),
    ]
