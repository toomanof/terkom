# Generated by Django 2.0.5 on 2018-07-23 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0043_auto_20180723_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='dish',
        ),
    ]