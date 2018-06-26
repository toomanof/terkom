from ..models import Dish
from django.forms import ModelForm
from django.forms import Select, TextInput

class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'
        widgets ={
            'name':TextInput(attrs={'class': 'form-control mr-3'}),
            'unit':Select(attrs={'class': 'form-control mr-3'}),
            'out':TextInput(attrs={'class': 'form-control mr-3'}),
            'tech_map':Select(attrs={'class': 'form-control mr-3'}),
            
        }