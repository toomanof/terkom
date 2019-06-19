import logging
from django.urls import reverse
from django.contrib import admin
from django.db.models import Model
from django.db.models import CASCADE
from django.db.models import PROTECT
from django.db.models import Sum, Max
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import ForeignKey
from django.db.models import DecimalField
from django.db.models import DateTimeField
from django.db.models import PositiveIntegerField
from django.core.validators import validate_comma_separated_integer_list
from .dish import Dish


class Map(Model):

    name = CharField(verbose_name='название', max_length=250)
    source = CharField(verbose_name='источник', blank=True,
                       max_length=250, null=True)
    approved = ForeignKey('People', verbose_name='утверждено',
                          null=False, blank=True, default=None,
                          related_name='map_approved', on_delete=PROTECT)
    agreed = ForeignKey('People', verbose_name='согласовано',
                        null=False, blank=True, default=None,
                        related_name='map_agreed', on_delete=PROTECT)
    technology = TextField(verbose_name='технология приготовления')
    created_at = DateTimeField(verbose_name='создано',
                               auto_now_add=True)
    batch_output = CharField(verbose_name='выход порции',
                             validators=[
                                 validate_comma_separated_integer_list],
                             max_length=255, blank=True)
    unit = ForeignKey('Unit', verbose_name='ед. изм', null=True,
                      blank=True, default=None, on_delete=PROTECT)

    def __str__(self):
        return 'ТЕХНОЛОГИЧЕСКАЯ КАРТА:{}'.format(self.name)

    @property
    def netto(self):
        return self.items.aggregate(sum=Sum('netto'))['sum']

    @property
    def brutto(self):
        return self.items.aggregate(sum=Sum('brutto'))['sum']

    def save(self, *args, **kwargs):        
        self.name = self.name.capitalize()
        super(Map, self).save(*args, **kwargs)
        if not self.dish.exists():
            dish = Dish(tech_map=self)
        else:
            dish = self.dish.all()[0]

        dish.name = self.name
        dish.out = self.batch_output
        dish.unit = self.unit
        dish.save()

    def copy(self):

        new_map = self
        new_map.pk = None
        new_map.name += '_copy'
        new_map.save()
        for old_map_item in self.items.all():
            logging.error(old_map_item)
            new_map_item = MapItems(map_doc_id=new_map.pk,
                                    product=old_map_item.product,
                                    brutto=old_map_item.brutto,
                                    netto=old_map_item.netto)
            new_map_item.save()
            logging.error(new_map_item)

    def get_absolute_url(self):
        return reverse('map-update', kwargs={'pk': self.pk})

    class Meta:
        app_label = 'calculation'
        verbose_name = 'Технологическая карта'
        verbose_name_plural = 'Технологические карты'
        ordering = ['name']


class MapItems(Model):

    map_doc = ForeignKey(Map, verbose_name='документ', null=False, blank=True,
                         default=None, on_delete=CASCADE, related_name='items')
    position = PositiveIntegerField(verbose_name='№', editable=False,
                                    db_index=True)
    product = ForeignKey('Dish', verbose_name='сырье',
                         null=False, blank=True, default=None,
                         on_delete=PROTECT)

    brutto = DecimalField(max_digits=15, decimal_places=3,
                          default=0, verbose_name='брутто')
    netto = DecimalField(max_digits=15, decimal_places=3,
                         blank=True, null=True,
                         default=0, verbose_name='неттто')

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        if not self.position:
            position = self.map_doc.items.aggregate(
                Max('position'))['position__max'] or 0
            self.position = position + 1
        super(MapItems, self).save(*args, **kwargs)


class MapItemsInline(admin.TabularInline):

    model = MapItems
    fields = (
        'position',
        'product',
        'brutto',
        'netto',
    )
    readonly_fields = ('position',)
    ordering = ['position']


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    fieldsets = (('', {'fields': (('name', 'source'),
                                  ('approved', 'agreed'),
                                  ('batch_output', 'unit', 'technology'))
                       }),
                 )

    inlines = [
        MapItemsInline,
    ]
    list_display = ('name', 'approved', 'agreed',)
    search_fields = ('name', 'source',)
    list_display_links = ('name',)
