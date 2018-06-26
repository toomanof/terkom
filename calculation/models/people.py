from django.urls import reverse
from django.contrib import admin
from django.db.models import Model
from django.db.models import CharField


class People(Model):
    first_name = CharField(max_length=100, verbose_name=' Имя')
    second_name = CharField(max_length=100, verbose_name=' Отчество')
    last_name = CharField(max_length=100, verbose_name=' Фамилия')
    
    def __str__(self):
        return '{} {}.{}.'.format(self.last_name.title(),
            self.first_name[0].upper(),
            self.second_name[0].upper())

    def get_absolute_url(self):
        return reverse('people-update', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'appcalc_peoples'
        app_label = 'calculation'
        verbose_name = 'Физ. лица'
        verbose_name_plural = 'Физ. лица'
        ordering = ['last_name','first_name','last_name']
        unique_together = (('last_name','first_name','last_name'),)

@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','last_name',)
    search_fields = ('last_name','first_name','last_name',)
    list_display_links =('last_name','first_name','last_name',)