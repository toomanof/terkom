from ..models import Product
from django.forms import ModelForm
from django.forms import Select, TextInput, NumberInput

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets ={
            'name':TextInput(attrs={'class': 'form-control ml-3 mr-3',
            	                    'required':True,
            	                    'data-msg':'Не указано название'}),
            'dish':Select(attrs={'class': 'form-control ml-3',
                                 'required':True,
                                 'data-msg':'Количество не указано' }),
            'unit':Select(attrs={'class': 'form-control ml-3 mr-3'}),
            'weight':NumberInput(attrs={'class': 'form-control ml-3 mr-3',
            	                        'required':True,
            	                        'data-msg':'Не указан вес за \
            	                        единицу продукции'}),
        }