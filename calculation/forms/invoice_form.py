from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms import CharField, TextInput, ModelChoiceField,NumberInput
from django.forms import DateField, DateInput,Select
from ..models import Invoice, InvoiceItems
from root import settings

    

class InvoiceItemsForm(ModelForm):
    
    class Meta:
        model = InvoiceItems
        fields = ['product','qty','price']
        widgets ={
            'product':Select(attrs={'class': 'form-control', 'required':True, 'data-msg':'Укажите продукт'}),
            'qty':NumberInput(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Количество не указано'}),
            'price':NumberInput(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Цена не указана'}),
        }

InvoiceItemsFormSet = inlineformset_factory(Invoice,
                                 InvoiceItems,
                                 form=InvoiceItemsForm,
                                 fk_name='invoce_doc',
                                 extra=1)

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['number','created_at',
                  'contractor','delivered',
                   'adopted','motion']
        widgets ={
            'created_at':DateInput(attrs={'class': 'form-control mr-3',
                                          'required':True,
                                          'data-msg':'Укажите дату накладной'}),
            'contractor':Select(attrs={'class': 'form-control mr-3',
                                       'required':True,
                                       'data-msg':'Количество не указано'}),
            'delivered':Select(attrs={'class': 'form-control mr-3'}),
            'adopted':Select(attrs={'class': 'form-control mr-3'}),
            'motion':Select(attrs={'class': 'form-control mr-3'}),
        }