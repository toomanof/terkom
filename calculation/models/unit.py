from django.contrib import admin
from django.db.models import Model
from django.db.models import SlugField
from django.db.models import CharField


class Unit(Model):
    short_name = CharField(max_length=50,
                           verbose_name='краткое название')
    full_name = CharField(max_length=250,
                          verbose_name='полное название')
    code = SlugField(max_length=4, verbose_name='код', unique=True)

    def __str__(self):
        return self.short_name

    class Meta:
        db_table = 'appcalc_units'
        app_label = 'calculation'
        verbose_name = 'Единицы измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ['code']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('code', 'short_name', 'full_name')
    search_fields = ('code', 'short_name', 'full_name')
    list_display_links = ('code',)
    list_editable = ('short_name', 'full_name')
