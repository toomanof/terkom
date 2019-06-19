import logging
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse_lazy

from ..models import Map, MapItems, Dish
from ..forms import MapForm, MapItemsFormSet
from .views import ActionVew, ListViewFor, DeleteViewMixin


@csrf_exempt
def yield_dish(request, **kwargs):  
    data = {'out':0}
    dish  = Dish.objects.filter(id=int(kwargs['dish']))
    if dish:        
        data = {'out':dish[0].out}
    return JsonResponse(data)

def map_copy(request, **kwargs):
    print(kwargs)
    map = Map.objects.get(pk=kwargs['pk'])
    new_map = map
    new_map.name +='_copy'
    new_map.source = map.source
    new_map.approved = map.approved
    new_map.agreed = map.agreed
    new_map.technology = map.technology
    new_map.created_at = map.created_at
    new_map.batch_output = map.batch_output
    new_map.unit = map.unit
    new_map.save()
    for old_map_item in map.items.all():
        print('old_map_item',old_map_item)
        new_map_item = MapItems(map_doc_id=new_map.id,
                                product=old_map_item.product,
                                brutto=old_map_item.brutto,
                                netto= old_map_item.netto)
        new_map_item.save()
        print('ID NEW map ',new_map.id)
        print('new_map_item', new_map_item.id)
    return redirect('map-list')

class MapsView(ListViewFor, ListView):
    model = Map
    paginate_by = 100
    template_name = 'list/map_list.html'
        

class MapCreateView(ActionVew, CreateView):
    
    action = 0
    model = Map
    form_class = MapForm
    template_name = 'element/map.html'
    success_url = reverse_lazy('map-list')
    parent_href = reverse_lazy('map-list')

    def get_context_data(self, **kwargs):
        context = super(MapCreateView, self).get_context_data(**kwargs)
        context['rows'] = MapItemsFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        rows = MapItemsFormSet(self.request.POST)
        if form.is_valid() and rows.is_valid():
            try:
                return self.form_valid(form, rows)
            except IntegrityError:
                pass
        return self.form_invalid(form, rows)

    def form_valid(self, form, rows):
        self.object = form.save()
        rows.instance = self.object
        fs_not_save = rows.save(commit=False)
        for form in fs_not_save:
            if form.product_id:
                form.save()
        messages.success(self.request,
                         'Сохранение прошло успешно!')        
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form, rows):
        for error in rows.errors:
            messages.error(self.request,error)
        return self.render_to_response(self.get_context_data(form=form,
                                                             rows=rows))    


class MapView(ActionVew, UpdateView):
    
    action = 1
    model = Map
    form_class = MapForm
    template_name = 'element/map.html'
    #success_url = reverse_lazy('map-list')
    parent_href = reverse_lazy('map-list')

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['rows'] = MapItemsFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        rows = MapItemsFormSet(self.request.POST, instance=self.object)
        if form.is_valid() and rows.is_valid():
            return self.form_valid(form, rows)
        return self.form_invalid(form, rows)

    def form_valid(self, form, rows):
        self.object = form.save()
        print('form is valid')
        rows.instance = self.object
        rows.save()

        fs_not_save = rows.save(commit=False)
        for row in fs_not_save:
            if row.product_id:
                row.save()
        messages.success(self.request,
                         'Сохранение прошло успешно!')
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form, rows):
        print('form is invalid')
        for key, val in form.errors.items():
            messages.error(self.request, '{} {}'.format(key,val))
        for error in rows.errors:
            messages.error(self.request,error)
        return self.render_to_response(self.get_context_data(form=form,
                                                             rows=rows))

class DeleteMapView(DeleteViewMixin, DeleteView):
    
    model = Map    
    success_url = reverse_lazy('map-list')
    template_name ='confirm_delete.html'