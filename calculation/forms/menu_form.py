from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms import Select, TextInput, HiddenInput
from ..models import Menu, MenuItems


class MenuItemsForm(ModelForm):

    class Meta:
        model = MenuItems
        fields = ['dish', 'out']
        widgets = {'dish': Select(attrs={'class': 'form-control mr-3',
                                         'required': True,
                                         'data-msg': 'Укажите блюдо'}),
                   'out': TextInput(attrs={'class': 'form-control mr-3',
                                           'required': True,
                                           'data-msg': 'Укажите вес блюда'})
                   }


MenuItemsFormSet = inlineformset_factory(Menu, MenuItems,
                                         form=MenuItemsForm,
                                         fk_name='invoce_doc',
                                         extra=1)


class MenuForm(ModelForm):

    class Meta:
        model = Menu
        fields = ['created_at', 'approved', 'food_intake']
        widgets = {'created_at': HiddenInput(attrs={}),
                   'food_intake': Select(attrs={'class': 'form-control mr-3',
                                                'required': True,
                                                'data-msg': 'Укажите период'})
                   }
