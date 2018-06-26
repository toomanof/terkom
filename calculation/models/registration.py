import datetime
from django.contrib import admin
from django.db.models import Model
from django.db.models import PROTECT
from django.db.models import ForeignKey
from django.db.models import DecimalField
from django.db.models import DateTimeField
from django.db.models import SmallIntegerField
from calculation.constants import ARRIVAL, EXPENSE, TYPE_CHOICES

class Registration(Model):

    invoce = ForeignKey('Invoice', verbose_name='накладная',
                        null=True, blank=True, default=None,
                        on_delete=PROTECT)    
    from_of = ForeignKey('Contractor', verbose_name='Котрагент',
                         null=False, blank=True, default=None,
                         on_delete=PROTECT)    
    product = ForeignKey('Product', verbose_name='товар',
                         null=False, blank=True, default=None,
                         on_delete=PROTECT)
    motion = SmallIntegerField(choices=TYPE_CHOICES, default=ARRIVAL)
    qty = DecimalField(max_digits=15, decimal_places=3,
                       default=0,verbose_name='количество')
    summa = DecimalField(max_digits=15, decimal_places=2,
                         default=0,verbose_name='сумма')
    created_at = DateTimeField(verbose_name ='создано',null=False,
                               db_index=True)
    class Meta:
        app_label = 'calculation'
        verbose_name = 'Запись регистра "Cклад"'
        verbose_name_plural = 'Регистр "Cклад"'
        ordering = ['product','created_at']

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('invoce', 'from_of', 'product', 'motion', 'summa',
                    'created_at')
    def has_add_permission(self, request):
        return False
    #def has_change_permission(self, request):
    #    return False            

    def has_delete_permission(self, request, obj=None):
        return False
