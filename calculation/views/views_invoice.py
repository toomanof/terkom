import logging
from ..constants import *
from .views import ActionVew, ListViewFor, DeleteViewMixin
from ..models import Invoice, InvoiceItems
from ..models import RegPrice
from ..forms import InvoiceForm, InvoiceItemsForm, InvoiceItemsFormSet
from ..forms import ProductForm

from django.contrib import messages 
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


def insert_or_update_price(product_id, created_at, price):
    if not RegPrice.objects.filter(product_id=product_id)\
                           .filter(created_at=created_at)\
                           .exists():
        RegPrice.objects.filter(created_at=created_at)\
                        .filter(product_id=product_id)\
                        .update(price=price)


class InvoicesView(ListViewFor, ListView):

    motion = ARRIVAL
    model = Invoice
    paginate_by = 100
    template_name = 'list/invoice_list.html'

    def get_queryset(self):
        return Invoice.objects.filter(motion=self.motion)

class InvoiceView(ActionVew, UpdateView):
    
    action = 1
    model = Invoice
    form_class = InvoiceForm
    template_name = 'element/invoice.html'
    parent_href = reverse_lazy('invoices-arrival-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rows'] = InvoiceItemsFormSet(instance=self.object)
        context['form_product'] = ProductForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        rows = InvoiceItemsFormSet(request.POST,
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
            if row.product_id:
                row.save()
        messages.success(self.request,
                         'Накладная сохранена!')
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form, rows):
        for error in rows.errors:
            messages.error(self.request,error)
        return self.render_to_response(self.get_context_data(form=form,
                                 rows=rows))

class InvoiceCreateView(ActionVew, CreateView):
    
    action = 0
    model = Invoice
    form_class = InvoiceForm
    template_name = 'element/invoice.html'
    parent_href = reverse_lazy('invoices-arrival-list')

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        logging.error(self.request)
        if self.request.method == 'POST':            
            context['rows'] = InvoiceItemsFormSet(instance=None)
        else:
            context['rows'] = InvoiceItemsFormSet(instance=self.object)
        context['form_product'] = ProductForm()
        return context

    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        rows = InvoiceItemsFormSet(request.POST)
        if form.is_valid() and rows.is_valid():
            return self.form_valid(form, rows)
        return self.form_invalid(form, rows)

    def form_valid(self, form, rows):
        logging.error(form)
        self.object = form.save()
        rows.instance = self.object
        fs_not_save = rows.save(commit=False)
        for row in fs_not_save:
            if row.product_id:
                row.save()        
                reg_price = RegPrice(product_id=row.product_id,
                                     price=row.price,
                                     created_at=self.object.created_at)
                reg_price.save()

        return  super(self.__class__, self).form_valid(form)
    
    def form_invalid(self, form, rows):
        for error in rows.errors:
            messages.error(self.request,error)
        self.object= self.get_queryset()
        return super(self.__class__, self).form_invalid(form)


class InvoiceDeleteView(DeleteViewMixin, DeleteView):
    
    model = Invoice
    success_url = reverse_lazy('invoices-arrival-list')
    template_name ='confirm_delete.html'