from ..models import Map, MapItems
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms import Select, TextInput, Textarea,DateInput, NumberInput 


class MapItemsForm(ModelForm):
    class Meta:
        model = MapItems
        fields = ['product','brutto','netto']
        widgets ={
            'product':Select(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Укажите продукт'}),
            'brutto':NumberInput(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Укажите брутто'}),
            'netto':NumberInput(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Укажите нетто'}),
        }   
        

MapItemsFormSet = inlineformset_factory(Map,
                                 MapItems,
                                 form=MapItemsForm,
                                 fk_name='map_doc',
                                 extra=1)


class MapForm(ModelForm):
    class Meta:
        model = Map
        fields = '__all__'
        widgets ={
            'name':TextInput(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Не указано название'}),
            'source':TextInput(attrs={'class': 'form-control mr-3'}),
            'approved':Select(attrs={'class': 'form-control mr-3'}),
            'agreed':Select(attrs={'class': 'form-control mr-3'}),
            'technology':Textarea(attrs={'class': 'form-control mr-3'}),
            'created_at':DateInput(attrs={'class': 'form-control mr-3'}),
            'batch_output':TextInput(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Не указан выход продукции'}),
            'unit':Select(attrs={'class': 'form-control mr-3'}),
            
        }