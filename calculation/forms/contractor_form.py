from ..models import Contractor
from django.forms import ModelForm
from django.forms import Select, TextInput

class ContractorForm(ModelForm):
    class Meta:
        model = Contractor
        fields = '__all__'
        widgets ={
            'name':TextInput(attrs={'class': 'form-control mr-3'}),
            'type_c':Select(attrs={'class': 'form-control mr-3'}),   
        }