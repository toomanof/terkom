from django.contrib import messages
from django.db.models import ProtectedError

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse
from django.urls import reverse_lazy

from ..models import Dish
from ..models import Product
from ..models import People
from ..models import Contractor

from ..forms import DishForm, ProductForm, PeopleForm, ContractorForm
from ..constants import *


def update_products(request):
    products = Product.objects.filter(dish_id__isnull=True)
    for product in products:
        dish = Dish.objects.get(name=product.name)
        if dish:
            Product.objects.filter(id=product.id).update(dish=dish)
    return redirect('product-list')

def redirect_to(request):
    return redirect('calculations')


@csrf_exempt
def create_dish(request, **kwargs):
    if 'name' in kwargs:
        new_dish = Dish(name=kwargs['name'])
        new_dish.save()
        data = {'dish_id': new_dish.id}
    return JsonResponse(data)


@csrf_exempt
def create_product(request, **kwargs):
    if request.POST:
        new_product = Product()
        new_product.name = request.POST['name']
        new_product.dish_id = request.POST['dish']
        new_product.unit_id = request.POST['unit']
        new_product.weight = request.POST['weight']
        new_product.save()
    return JsonResponse({'key': new_product.id, 'name': new_product.name})

#-----------     Additional Classes   ----------------------


class ActionVew(View):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'action'):
            context['parent_title'] = self.model._meta.\
                verbose_name_plural.title()
            context['parent_href'] = self.parent_href
            context['success_url'] = getattr(self, 'success_url', '')
            context['action'] = '{} карточки:"{}"'.\
                format(ACTIONS[self.action],
                       self.model._meta.
                       verbose_name.lower())

        return context


class ListViewFor(View):
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super(ListViewFor, self).get_context_data(**kwargs)
        context['parent_title'] = TITLE_MAIN_PAGE

        context['success_url'] = reverse('main_calculation')
        context['title'] = self.model._meta.verbose_name_plural.title()
        return context


class DeleteViewMixin(View):

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(request, messages.ERROR,
                                 'Запись задействована, и \
                                  не может быть удалена!')

            return HttpResponseRedirect(self.object.get_absolute_url())


#-----------     Menu    ----------------------


#-----------     Dish    ----------------------

class DishsView(ListViewFor, ListView):
    model = Dish
    paginate_by = 100
    template_name = 'list/dish_list.html'


class DishCreateView(ActionVew, CreateView):

    action = 0
    model = Dish
    form_class = DishForm
    template_name = 'element/dish.html'
    parent_href = reverse_lazy('dish-list')


class DishView(ActionVew, UpdateView):

    action = 1
    model = Dish
    form_class = DishForm
    template_name = 'element/dish.html'
    parent_href = reverse_lazy('dish-list')


class DeleteDishView(DeleteViewMixin, DeleteView):

    model = Dish
    success_url = reverse_lazy('dish-list')
    template_name = 'confirm_delete.html'

#-----------     Product     ----------------------


class ProductsView(ListViewFor, ListView):

    model = Product
    paginate_by = 100
    template_name = 'list/product_list.html'


class ProductCreateView(ActionVew, CreateView):

    action = 0
    model = Product
    form_class = ProductForm
    template_name = 'element/product.html'
    success_url = reverse_lazy('product-list')
    parent_href = reverse_lazy('product-list')


class ProductView(ActionVew, UpdateView):

    action = 1
    model = Product
    form_class = ProductForm
    template_name = 'element/product.html'
    success_url = reverse_lazy('product-list')
    parent_href = reverse_lazy('product-list')


class DeleteProductView(DeleteViewMixin, DeleteView):

    model = Product
    success_url = reverse_lazy('product-list')
    template_name = 'confirm_delete.html'

#-----------     People     ----------------------


class PeoplesView(ListViewFor, ListView):
    model = People
    paginate_by = 100
    template_name = 'list/people_list.html'


class PeopleCreateView(ActionVew, CreateView):

    action = 0
    model = People
    form_class = PeopleForm
    template_name = 'element/people.html'
    parent_href = reverse_lazy('people-list')


class PeopleView(ActionVew, UpdateView):

    action = 1
    model = People
    form_class = PeopleForm
    template_name = 'element/people.html'
    parent_href = reverse_lazy('people-list')


class DeletePeopleView(DeleteViewMixin, DeleteView):

    model = People
    success_url = reverse_lazy('people-list')
    template_name = 'confirm_delete.html'

#-----------     Contractor     ----------------------


class ContractorsView(ListViewFor, ListView):
    model = Contractor
    paginate_by = 100
    template_name = 'list/contractor_list.html'


class ContractorCreateView(ActionVew, CreateView):

    action = 0
    model = Contractor
    form_class = ContractorForm
    template_name = 'element/contractor.html'
    parent_href = reverse_lazy('contractor-list')


class ContractorView(ActionVew, UpdateView):

    action = 1
    model = Contractor
    form_class = ContractorForm
    template_name = 'element/contractor.html'
    parent_href = reverse_lazy('contractor-list')


class DeleteContractorView(DeleteViewMixin, DeleteView):

    model = Contractor
    success_url = reverse_lazy('contractor-list')
    template_name = 'confirm_delete.html'
