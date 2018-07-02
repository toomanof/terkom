import logging
from datetime import date, datetime, timedelta
from calendar import monthrange

from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.urls import reverse_lazy

from ..constants import *
from ..models import Menu
from ..forms import MenuForm
from ..forms import MenuItemsFormSet
from .views import ActionVew, DeleteViewMixin


def get_menu(request, **kwargs):
    if 'pk' not in kwargs:
        return MenuCreateView.as_view(**kwargs)(request)


def delete_menu(request, **kwargs):
    Menu.objects.all().delete()
    return reverse_lazy('menu-list')


def copy_menu(request, **kwargs):
    '''    print(kwargs)
        if kwargs:
            date_menu = date(int(kwargs['year']),
                             int(kwargs['month']),
                             int(kwargs['day']))
            plus_day = 0
            if 'copy' in kwargs and kwargs['copy'] == COPY_TO_TOMORROW:
                plus_day = 1
            if 'copy' in kwargs and kwargs['copy'] == COPY_TO_MONTH:
                current_month = monthrange(
                    int(kwargs['year']), int(kwargs['month']))
                plus_day = current_month[1] - date_menu.day

            for delta_day in range(1, plus_day + 1):
                menus_in_date = Menu.objects.filter(created_at=date_menu)
                for menu_in_date in menus_in_date:
                    try:
                        menu_in_date.pk = None
                        menu_in_date.created_at = date_menu + timedelta(delta_day)
                        menu_in_date.save()
                    except Exception as e:
                        pass

        return redirect('menu-list')
    '''
    pass


class MenuCalendarView(TemplateView):

    template_name = 'list/menus.html'

    def get_context_data(self, **kwargs):
        context = super(MenuCalendarView, self).get_context_data(**kwargs)
        dates_menu = list(Menu.objects.values('id', 'created_at',
                                              'food_intake').distinct())

        dates_menu = [{'id':item['id'], 'created_at': item['created_at'],
                       'food_intake': TYPE_FOOD_INTAKE[item['food_intake']-1][1]}
                      for item in dates_menu]
        logging.error(dates_menu)
        context['dates_menu'] = dates_menu
        context['title'] = 'Календарь меню'
        context['parent_title'] = TITLE_MAIN_PAGE
        context['parent_href'] = reverse('main_calculation')
        return context


class MenuView(ActionVew, UpdateView):

    action = 1
    model = Menu
    form_class = MenuForm
    template_name = 'element/menu.html'
    parent_href = reverse_lazy('menu-list')
    year = ''
    month = ''
    day = ''

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['rows'] = MenuItemsFormSet(instance=self.object)
        context['created_at'] = self.object.created_at
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        rows = MenuItemsFormSet(request.POST,
                                instance=self.object)
        if form.is_valid() and rows.is_valid():
            return self.form_valid(form, rows)
        return self.form_invalid(form, rows)

    def form_valid(self, form, rows):
        self.object = form.save()
        rows.instance = self.object
        fs_not_save = rows.save(commit=False)
        for obj in rows.deleted_objects:
            obj.delete()
        for row in fs_not_save:
                row.save()
        messages.success(self.request,
                         'Меню сохранено!')
        return super(self.__class__, self).form_valid(form)

    def form_invalid(self, form, rows):
        for error in rows.errors:
            messages.error(self.request, error)
        return super(self.__class__, self).form_invalid(form)


class MenuCreateView(ActionVew, CreateView):

    action = 0
    model = Menu
    form_class = MenuForm
    template_name = 'element/menu.html'
    parent_href = reverse_lazy('menu-list')
    year = ''
    month = ''
    day = ''

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        instance = self.object if self.request.method == 'POST' else None
        context['rows'] = MenuItemsFormSet(instance=instance)
        context['created_at'] = date(int(self.year),
                                     int(self.month),
                                     int(self.day))
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        rows = MenuItemsFormSet(request.POST)

        if form.is_valid() and rows.is_valid():
            return self.form_valid(form, rows)
        return self.form_invalid(form, rows)

    def form_valid(self, form, rows):
        self.object = form.save()
        rows.instance = self.object
        fs_not_save = rows.save(commit=False)
        for obj in rows.deleted_objects:
            obj.delete()
        for row in fs_not_save:
                row.save()
        messages.success(self.request,
                         'Меню сохранено!')
        return super(self.__class__, self).form_valid(form)

    def form_invalid(self, form, rows):
        for error in rows.errors:
            messages.error(self.request, error)
        return super(self.__class__, self).form_invalid(form)


class MenuDeleteView(DeleteViewMixin, DeleteView):

    model = Menu
    success_url = reverse_lazy('menu-list')
    template_name = 'confirm_delete.html'
