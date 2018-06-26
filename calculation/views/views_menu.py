import logging
from datetime import date, datetime, timedelta
from calendar import monthrange

from django.contrib import messages
from django.views.generic import TemplateView
from django.urls import reverse
from django.shortcuts import render, redirect

from ..constants import *
from ..models import Menu
from ..forms import MenuFormSet


def delete_menu(request,**kwargs):
    if kwargs:
        date_menu = date(int(kwargs['year']),
                             int(kwargs['month']),
                             int(kwargs['day']))
        Menu.objects.filter(created_at=date_menu).delete()
    return redirect('menu-list')

def copy_menu(request,**kwargs):
    print(kwargs)
    if kwargs:
        date_menu = date(int(kwargs['year']),
                         int(kwargs['month']),
                         int(kwargs['day']))
        plus_day = 0
        if 'copy' in kwargs and kwargs['copy'] == COPY_TO_TOMORROW:
            plus_day = 1
        if 'copy' in kwargs and kwargs['copy'] == COPY_TO_MONTH:
            current_month = monthrange(int(kwargs['year']),int(kwargs['month']))
            plus_day =current_month[1] - date_menu.day 
        
        for delta_day in range(1,plus_day+1):
            menus_in_date = Menu.objects.filter(created_at=date_menu)
            for menu_in_date in menus_in_date:
                try:
                    menu_in_date.pk = None
                    menu_in_date.created_at = date_menu + timedelta(delta_day)
                    menu_in_date.save()
                except Exception as e:
                    pass

    return redirect('menu-list')

class MenuCalendarView(TemplateView):

    template_name = 'list/menus.html'
    def get_context_data(self, **kwargs):
        context = super(MenuCalendarView, self).get_context_data(**kwargs)
        dates_menu = Menu.objects.values('created_at').distinct()
        logging.error(dates_menu)
        context['dates_menu'] =dates_menu
        context['title'] = 'Календарь меню'
        context['parent_title'] = TITLE_MAIN_PAGE
        context['parent_href'] = reverse('main_calculation')
        return context

class MenuView(TemplateView):

    template_name = 'element/menu.html'
    def get_context_data(self, **kwargs):
        context = super(MenuView, self).get_context_data(**kwargs)
        date_menu = date(int(kwargs['year']),
                             int(kwargs['month']),
                             int(kwargs['day']))

        context['create'] = 'create' not in kwargs
        context['action'] = ACTIONS['create' not in kwargs]

        context['created_at'] = date_menu
        context['formset'] = MenuFormSet(queryset=
            Menu.objects.filter(created_at=date_menu))
        context['parent_title'] = 'Календарь меню'
        context['parent_href'] =reverse('menu-list')


        return context
    
    def post(self, request, **kwargs):
        date_menu = datetime.strptime(request.POST['created_at'],
                                      '%Y-%m-%d')
        formset = MenuFormSet(request.POST)
        kwargs['date_menu'] = date_menu.date()
        if formset.is_valid():
            return self.form_valid(formset, **kwargs)
        else:
            return self.form_invalid(formset, **kwargs)


    def form_valid(self, formset, **kwargs):
        fs_not_save = formset.save(commit=False)
        for form in fs_not_save:
            if form.dish_id:
                form.save()
                messages.success(self.request,
                                 'Блюдо:"{}" сохранено!'.\
                                  format(form.dish.name))

        return render(self.request, 
                      self.template_name,
                      {'formset': formset,
                       'created_at':kwargs['date_menu']})

    def form_invalid(self, form, **kwargs):  
        for error in form.errors:
            messages.error(self.request,error)
        return render(self.request, 
                      self.template_name,
                      {'formset': MenuFormSet(queryset=
                       Menu.objects.filter(created_at=kwargs['date_menu'])),
                       'created_at':kwargs['date_menu']})