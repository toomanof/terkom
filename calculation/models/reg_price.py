import datetime
from django.contrib import admin
from django.db.models import Model
from django.db.models import PROTECT
from django.db.models import ForeignKey
from django.db.models import DecimalField
from django.db.models import DateField

class RegPrice(Model):
    invoce = ForeignKey('Invoice', verbose_name='накладная',
                        null=True, blank=True, default=None,
                        on_delete=PROTECT)    
    product = ForeignKey('Product', verbose_name='продукт',
                         null=False, blank=True, default=None,
                         on_delete=PROTECT, db_index=True)
    price = DecimalField(max_digits=15, decimal_places=2,
                         default=0,verbose_name='цена')
    created_at = DateField(verbose_name ='создано', db_index=True)
    class Meta:
        db_table = 'calculation_regprice'
        app_label = 'calculation'
        verbose_name = 'Запись регистра "Цены"'
        verbose_name_plural = 'Регистр "Цены"'
        ordering = ['product','created_at']
        unique_together = (('product','created_at'),)



@admin.register(RegPrice)
class RegPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'created_at', 'invoce')

    def has_add_permission(self, request):
        return False
    #def has_change_permission(self, request):
    #    return False            

    #def has_delete_permission(self, request, obj=None):
    #    return False
