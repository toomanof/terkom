from django.urls import reverse
from django.contrib import admin
from django.db.models import Model
from django.db.models import CharField
from calculation.constants import TYPE_CHOICES_CONTRACTOR, OUTER, INTERIOR 


class Contractor(Model):
      
    name = CharField(max_length=250, verbose_name='Наименование')
    type_c = CharField(max_length=25, choices=TYPE_CHOICES_CONTRACTOR,
                    default=OUTER, verbose_name='Тип')

    def __str__(self):
        return '{} ({})'.format(self.name, self.type_c)

    def get_absolute_url(self):
        return reverse('contractor-update', kwargs={'pk': self.pk})
    class Meta:
        app_label = 'calculation'
        verbose_name = 'Котрагенты'
        verbose_name_plural = 'Котрагенты'
        ordering = ['name']
        unique_together = ('name',)

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('name','type_c',)
    search_fields = ('name',)
    увше_fields = ('name',)