from django.forms import modelformset_factory
from django.forms import Select, TextInput, NumberInput, HiddenInput
from ..models import Menu

MenuFormSet = modelformset_factory(Menu, fields=['created_at','food_intake','dish','out'],
    widgets={'created_at':HiddenInput(attrs={}),
             'food_intake':Select(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Укажите период'}),
             'dish':Select(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Укажите блюдо'}),
             'out':TextInput(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Укажите вес блюда'})},
    extra=1, can_delete=True)
