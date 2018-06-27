import datetime
import decimal
from django.urls import reverse
from django.contrib import admin
from django.db import connection
from django.db.models import Model
from django.db.models import CASCADE
from django.db.models import PROTECT
from django.db.models import Max
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import DecimalField
from django.db.models import DateField
from django.db.models import PositiveIntegerField
from django.db.models import SmallIntegerField
from django.db.models.signals import pre_delete 
from calculation.service.helpers import dictfetchall, post, delete
from calculation.constants import ARRIVAL, EXPENSE, TYPE_CHOICES




class Invoice(Model):

    number = CharField(verbose_name='номер', blank=True, max_length=50,
                       help_text='Номер накладной')
    created_at = DateField(verbose_name='создано', db_index=True)
    contractor = ForeignKey('Contractor', verbose_name='Котрагент',
                            null=True, blank=True, default=None,
                            on_delete=PROTECT)

    delivered = ForeignKey('People', verbose_name='сдал',
                           null=True, blank=True, default=None,
                           related_name='delivered', on_delete=PROTECT)
    adopted = ForeignKey('People', verbose_name='принял',
                         null=True, blank=True, default=None,
                         related_name='adopted', on_delete=PROTECT)
    motion = SmallIntegerField(choices=TYPE_CHOICES, default=ARRIVAL)

    def __init__(self, *args, **kwargs):
        self.created_at = datetime.datetime.now()
        super(Invoice, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)
        post(self)

    def delete(self, *args, **kwargs):
        delete(self)
        super(self.__class__, self).delete(*args, **kwargs)

    @property
    def total(self):
        cursor = connection.cursor()
        cursor.execute('SELECT *,SUM(`qty` * `price`) as sum \
                       FROM calculation_invoiceitems WHERE \
                       `invoce_doc_id` =%s', [self.pk])
        row = dictfetchall(cursor)
        return row[0]['sum']

    @property
    def rows(self):
        return self.items.all()
    
    def get_absolute_url(self):
        return reverse('invoice-update', kwargs={'pk': self.pk})
    
    def get_success_url(self):
        return reverse_lazy('invoices-arrival-list')        

    class Meta:
        app_label = 'calculation'
        verbose_name = 'Накладные'
        verbose_name_plural = 'Накладные'
        ordering = ['number', 'created_at']
        unique_together = (('number', 'created_at',),)


class InvoiceItems(Model):

    invoce_doc = ForeignKey(Invoice, verbose_name='документ',
                            null=False, blank=True, default=None,
                            on_delete=CASCADE, related_name='items')
    position = PositiveIntegerField(verbose_name='№', editable=False,
                                    db_index=True)
    product = ForeignKey('Product', verbose_name='товар',
                         null=False, blank=True, default=None,
                         on_delete=PROTECT)
    qty = DecimalField(max_digits=15, decimal_places=3,
                       default=0, verbose_name='количество')
    price = DecimalField(max_digits=15, decimal_places=2,
                         default=0, verbose_name='цена')

    @property
    def summa(self):
      return self.qty * self.price

    def save(self, *args, **kwargs):
        if not self.position:
            position = self.invoce_doc.items.aggregate(
                Max('position'))['position__max'] or 0
            self.position = position + 1
        super(InvoiceItems, self).save(*args, **kwargs)

class InvoiceItemsInline(admin.TabularInline):

    model = InvoiceItems
    fields = (
        'position',
        'product',
        'qty',
        'price',
    )
    readonly_fields = ('position',)
    ordering = ['position']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    inlines = [
        InvoiceItemsInline,
    ]

    fieldsets = (
                 ('', {'fields': (('number', 'created_at', 'motion'),
                       ('contractor',), ('delivered', 'adopted'))}
                  ),
                 )

    list_display = ('number', 'created_at', 'contractor',
                    'delivered', 'adopted', 'total')
    search_fields = ('number', 'created_at',)
    list_display_links = ('number', 'created_at',)
