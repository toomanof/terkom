import base64
import pickle
from django.db.models import Model
from django.db.models import PROTECT
from django.db.models import TextField
from django.db.models import ForeignKey
from django.db.models import DateTimeField
from django.db.models import PositiveIntegerField


class Calculation(Model):

    qty_children = PositiveIntegerField()
    created_at = DateTimeField(verbose_name='создано', db_index=True)
    dish = ForeignKey('Dish', verbose_name='блюдо',
                      null=True, blank=True, default=None,
                      on_delete=PROTECT)
    values = TextField(verbose_name='',default='gAN9cQAu')
    food_intake = PositiveIntegerField(verbose_name='приём пищи', db_index=True)
    
    @property
    def number_of_food_products(self):
        return pickle.loads(base64.b64decode(self.values))

    def set_number_of_food_products(self):
        self.values = base64.b64encode(pickle.dumps(self.dish.ingredients))