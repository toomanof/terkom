import logging
from ..constants import *
from .views import ActionVew, ListViewFor, DeleteViewMixin
from ..models import Invoice
from ..models import RegPrice
from ..forms import InvoiceForm, InvoiceItemsFormSet
from ..forms import ProductForm

from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


def insert_or_update_price(product_id, created_at, price):
    reg_price = RegPrice.objects.filter(product_id=product_id)\
                                .filter(created_at=created_at)
    if reg_price:
        reg_price.update(price=price)


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
        #self.object = form.save()
        rows.instance = self.object
        fs_not_save = rows.save(commit=False)
        for obj in rows.deleted_objects:
            obj.delete()
        for row in fs_not_save:
            if row.product_id:
                row.save()
        messages.success(self.request,
                         'Накладная сохранена!')
        return super(self.__class__, self).form_valid(form)

    def form_invalid(self, form, rows):
        for error in rows.errors:
            messages.error(self.request, error)
        return super(self.__class__, self).form_invalid(form)

    def get_success_url(self, **kwargs):
        inv = self.get_object()
        if inv.motion == ARRIVAL:
            return reverse_lazy('invoices-arrival-list')            
        else:
            return reverse_lazy('invoices-consumption-list')


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
        #logging.error(form)
        self.object = form.save()
        rows.instance = self.object
        fs_not_save = rows.save(commit=False)
        for obj in rows.deleted_objects:
            obj.delete()
        for row in fs_not_save:
            if row.product_id:
                row.save()
        return super(self.__class__, self).form_valid(form)

    def form_invalid(self, form, rows):
        for error in rows.errors:
            messages.error(self.request, error)
        self.object = self.get_queryset()
        return super(self.__class__, self).form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('invoices-arrival-list')


class InvoiceDeleteView(DeleteViewMixin, DeleteView):

    model = Invoice
    template_name = 'confirm_delete.html'
    
    def get_success_url(self, **kwargs):
        inv = self.get_object()
        if inv.motion == ARRIVAL:
            return reverse_lazy('invoices-arrival-list')            
        else:
            return reverse_lazy('invoices-consumption-list')
