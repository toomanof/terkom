from django.urls import reverse
from django.contrib import admin
from django.db.models import Model
from django.db.models import CharField
from django.db.models import DecimalField
from django.db.models import ForeignKey
from django.db.models import PROTECT
from .dish import Dish


class Product(Model):
    name = CharField(max_length=250, verbose_name='Название')
    unit = ForeignKey('Unit', verbose_name='ед. изм', null=True,
                      blank=True, default=None, on_delete=PROTECT)
    dish = ForeignKey('Dish', verbose_name='продукт', null=True,
                      related_name='product', blank=True, default=None,
                      on_delete=PROTECT)
    weight = DecimalField(max_digits=15, decimal_places=3,
                          verbose_name='вес в килограммах одной единицы',
                          default=1, null=True)
    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Product, self).save(*args, **kwargs)
        if not self.dish:
            dish = Dish()
            dish.name = self.name
            dish.unit = self.unit
            dish.product = self
            dish.save()
#        if Dish.objects.filter(product=self).exists():
#            Dish.objects.filter(product=self).update(name = self.name,
#                                                 unit = self.unit)
#        else:

    def get_absolute_url(self):
        return reverse('product-update', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'appcalc_products'
        app_label = 'calculation'
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатура'
        ordering = ['name']
        unique_together = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'weight',)
    search_fields = ('name', 'unit',)
    list_display_links = ('name', 'unit',)
