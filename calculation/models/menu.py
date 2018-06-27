
from django.contrib import admin
from django.db import connection
from django.db.models import Model
from django.db.models import PROTECT
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import ForeignKey
from django.db.models import BooleanField
from django.db.models import PositiveIntegerField
from django.core.validators import validate_comma_separated_integer_list
from calculation.service.helpers import dictfetchall
from calculation.constants import TYPE_FOOD_INTAKE
from datetime import datetime


class Menu(Model):

    created_at = DateField(verbose_name='создано', db_index=True)
    approved = ForeignKey('People', verbose_name='утверждено',
                          null=True, blank=True, default=None,
                          related_name='menu_approved', on_delete=PROTECT)
    food_intake = PositiveIntegerField(verbose_name='приём пищи', default=1,
                                       db_index=True, choices=TYPE_FOOD_INTAKE)
    dish = ForeignKey('Dish', verbose_name='блюдо',
                      null=False, blank=True, default=None,
                      related_name='menu_dish', on_delete=PROTECT)
    out = CharField(verbose_name='выход порции', null=True,
                    validators=[validate_comma_separated_integer_list],
                    max_length=255, blank=True)
    in_action = BooleanField(verbose_name='в действии', default=True,
                             db_index=True)

    @property
    def total(self):
        cursor = connection.cursor()
        cursor.execute('SELECT *,SUM(`qty` * `price`) as sum \
                        FROM calculation_invoiceitems \
                        WHERE `invoce_doc_id` =%s', [self.pk])
        row = dictfetchall(cursor)
        return row[0]['sum']


    class Meta:
        app_label = 'calculation'
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ['created_at', 'food_intake']
        unique_together = (('created_at', 'food_intake', 'dish',),)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    list_display = ('created_at', 'food_intake', 'dish', 'out', 'in_action')
    search_fields = ('created_at', 'dish', 'food_intake')
    list_display_links = ('created_at',)