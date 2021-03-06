# Generated by Django 2.0.5 on 2018-06-02 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0005_auto_20180531_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name=' название')),
                ('out', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='выход')),
            ],
            options={
                'verbose_name': 'Блюда',
                'ordering': ['name'],
                'db_table': 'appcalc_courses',
                'verbose_name_plural': 'Юлюда',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, verbose_name='создано')),
                ('food_intake', models.PositiveIntegerField(db_index=True, verbose_name='приём пищи')),
                ('out', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='выход')),
                ('in_action', models.BooleanField(db_index=True, default=True, verbose_name='в действии')),
                ('approved', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, related_name='menu_approved', to='calculation.People', verbose_name='утверждено')),
                ('dish', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, related_name='menu_dish', to='calculation.Dish', verbose_name='утверждено')),
            ],
            options={
                'verbose_name': 'Меню',
                'ordering': ['created_at', 'food_intake'],
                'verbose_name_plural': 'Меню',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motion', models.SmallIntegerField(choices=[(1, 'arrival'), (-1, 'expense')], default=1)),
                ('qty', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='количество')),
                ('summa', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='сумма')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='создано')),
                ('from_of', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, to='calculation.Сontractor', verbose_name='Котрагент')),
                ('invoce', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='calculation.Invoice', verbose_name='накладная')),
                ('menu', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='calculation.Menu', verbose_name='меню')),
            ],
        ),
        migrations.AlterModelOptions(
            name='map',
            options={'ordering': ['number', 'created_at'], 'verbose_name': 'Технологическая карта', 'verbose_name_plural': 'Технологические карты'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterField(
            model_name='map',
            name='agreed',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, related_name='map_agreed', to='calculation.People', verbose_name='согласовано'),
        ),
        migrations.AlterField(
            model_name='map',
            name='approved',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, related_name='map_approved', to='calculation.People', verbose_name='утверждено'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='invoce',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='calculation.Invoice', verbose_name='накладная'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='motion',
            field=models.SmallIntegerField(choices=[(1, 'arrival'), (-1, 'expense')], default=1),
        ),
        migrations.AddField(
            model_name='registration',
            name='product',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, to='calculation.Product', verbose_name='товар'),
        ),
        migrations.AddField(
            model_name='dish',
            name='tech_map',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='course', to='calculation.Map', verbose_name='технологическая карта'),
        ),
        migrations.AddField(
            model_name='dish',
            name='unit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='calculation.Unit', verbose_name='ед. изм'),
        ),
    ]
