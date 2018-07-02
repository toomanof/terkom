from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import admin
from django.db.models import Model
from django.db.models import CASCADE
from django.db.models import PROTECT
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import ForeignKey
from django.db.models import BooleanField
from django.db.models import PositiveIntegerField
from django.core.validators import validate_comma_separated_integer_list
from calculation.constants import TYPE_FOOD_INTAKE


class Menu(Model):

    created_at = DateField(verbose_name='создано', db_index=True)
    approved = ForeignKey('People', verbose_name='утверждено',
                          null=True, blank=True, default=None,
                          related_name='menu_approved', on_delete=PROTECT)
    food_intake = PositiveIntegerField(verbose_name='приём пищи', default=1,
                                       db_index=True, choices=TYPE_FOOD_INTAKE)
    in_action = BooleanField(verbose_name='в действии', default=True,
                             db_index=True)


    def get_absolute_url(self):
        return reverse('menu-update', kwargs={'pk': self.pk})

    def get_success_url(self):
        return reverse_lazy('menu-list')

    class Meta:
        app_label = 'calculation'
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ['created_at', 'food_intake']


class MenuItems(Model):
    invoce_doc = ForeignKey(Menu, verbose_name='меню',
                            null=False, blank=True, default=None,
                            on_delete=CASCADE, related_name='items')
    dish = ForeignKey('Dish', verbose_name='блюдо',
                      null=False, blank=True, default=None,
                      related_name='menu_dish', on_delete=PROTECT)
    out = CharField(verbose_name='выход порции', null=True,
                    validators=[validate_comma_separated_integer_list],
                    max_length=255, blank=True)

    class Meta:
        app_label = 'calculation'
        verbose_name = 'комплектующие меню'
        verbose_name_plural = 'комплектующие меню'
        ordering = ['invoce_doc', 'dish']


class MenuItemsInline(admin.TabularInline):

    model = MenuItems
    fields = (
        'dish',
        'out',
    )
    ordering = ['dish']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    list_display = ('created_at', 'food_intake', 'in_action')
    search_fields = ('created_at', 'food_intake')
    list_display_links = ('created_at',)
