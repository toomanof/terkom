import logging
from django.urls import reverse
from django.contrib import admin
from django.db.models import Model
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import PROTECT
from django.core.validators import validate_comma_separated_integer_list


class Dish(Model):
    name = CharField(max_length=250, verbose_name=' название')
    unit = ForeignKey('Unit', verbose_name='ед. изм', null=True,
                      blank=True, default=None, on_delete=PROTECT)
    out = CharField(verbose_name='выход порции', null=True,
                    validators=[validate_comma_separated_integer_list],
                    max_length=255, blank=True)
    tech_map = ForeignKey('Map', verbose_name='технологическая карта',
                          related_name='dish', null=True, blank=True,
                          default=None, on_delete=PROTECT)

    def __str__(self):
        return self.name

    @property
    def ingredients(self):
        items = []
        if self.tech_map:
            items = self.tech_map.items.all()
        return items

    @property
    def product(self):
        return self.product

    def get_absolute_url(self):
        return reverse('dish-update', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'appcalc_courses'
        app_label = 'calculation'
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['name']


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'out', 'tech_map')
    search_fields = ('name', 'unit', 'tech_map')
    list_display_links = ('name',)
