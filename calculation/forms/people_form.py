from ..models import People
from django.forms import ModelForm
from django.forms import Select, TextInput

class PeopleForm(ModelForm):
    class Meta:
        model = People
        fields = '__all__'
        widgets ={
            'first_name':TextInput(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Забыли имя'}),
            'second_name':TextInput(attrs={'class': 'form-control mr-3'}),
            'last_name':TextInput(attrs={'class': 'form-control mr-3', 'required':True, 'data-msg':'Забыли фамилию'}),
        }