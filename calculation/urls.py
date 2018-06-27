from django.conf.urls import url
from .views.views_menu import MenuCalendarView, MenuView
from .views.views_menu import delete_menu, copy_menu
from .views.views import DishCreateView, DishView, DeleteDishView, DishsView
from .views.views_map import MapCreateView, MapView, MapsView, DeleteMapView
from .views.views_map import yield_dish, map_copy
from .views.views import ProductCreateView, ProductView, ProductsView
from .views.views import DeleteProductView
from .views.views import PeopleCreateView, PeopleView, PeoplesView
from .views.views import DeletePeopleView
from .views.views import ContractorCreateView, ContractorView, ContractorsView
from .views.views import DeleteContractorView
from .views.views_reports import CalculationView, CalculationPdfView
from .views.views_reports import ReportProductAccounting
from .views.views import redirect_to, create_dish, create_product
from .views.views import update_products
from .views.views_invoice import InvoiceView, InvoicesView, InvoiceCreateView
from .views.views_invoice import InvoiceDeleteView
from .constants import *


urlpatterns = [
    url(r'^$', redirect_to, name='main_calculation'),

    url(r'^report/prod_accounting/(?P<from_day>\d{2})\.(?P<from_month>\d{2})'
        '\.(?P<from_year>\d{4})-'
        '(?P<to_day>\d{2})[.-]{1}(?P<to_month>\d{2})[.-]{1}(?P<to_year>\d{4})',
        ReportProductAccounting.as_view(), name='report_pa_period'),

    url(r'^report\/prod_accounting/?$',
        ReportProductAccounting.as_view(), name='report_pa'),

    url(r'^calculations/(?P<year>\d{4})[.-]{1}'
        '(?P<month>\d{2})[.-]{1}(?P<day>\d{2})'
        '\/(?P<childrens>\d{1,3})$',
        CalculationView.as_view(), name='calculations_day'),

    url(r'^calculations/(?P<year>\d{4})[.-]{1}'
        '(?P<month>\d{2})[.-]{1}(?P<day>\d{2})'
        '\/(?P<childrens>\d{1,3})/pdf$',
        CalculationPdfView.as_view(), name='calculations_day_pdf'),

    url(r'^calculations/?$',
        CalculationView.as_view(), name='calculations'),


    url(r'^invoices/arrival/?$',
        InvoicesView.as_view(motion=ARRIVAL),
        name='invoices-arrival-list'),

    url(r'^invoices/consumption/?$',
        InvoicesView.as_view(motion=EXPENSE),
        name='invoices-consumption-list'),

    url(r'^invoice/(?P<pk>\d+)/update/?$',
        InvoiceView.as_view(),
        name='invoice-update'),

    url(r'^invoice/(?P<pk>\d+)/delete/?$',
        InvoiceDeleteView.as_view(),
        name='invoice-delete'),

    url(r'^invoice/add\/?$',
        InvoiceCreateView.as_view(),
        name='invoice-new'),


    url(r'^dishs/?$', DishsView.as_view(), name='dish-list'),

    url(r'^dish/add/?$', DishCreateView.as_view(), name='dish-new'),

    url(r'^dish/(?P<pk>\d+)/update/?$', DishView.as_view(), name='dish-update'),

    url(r'^dish/(?P<pk>\d+)/delete/?$',
        DeleteDishView.as_view(), name='dish-delete'),


    url(r'^maps/?$', MapsView.as_view(), name='map-list'),

    url(r'^map/add/?$', MapCreateView.as_view(), name='map-new'),

    url(r'^map/(?P<pk>\d+)/update/?$', MapView.as_view(), name='map-update'),
    url(r'^map/(?P<pk>\d+)/copy/?$', map_copy, name='map-copy'),

    url(r'^map/(?P<pk>\d+)/delete/?$', DeleteMapView.as_view(),
        name='map-delete'),

    url(r'^products/?$', ProductsView.as_view(), name='product-list'),

    url(r'^product/add/?$', ProductCreateView.as_view(), name='product-new'),

    url(r'^product/(?P<pk>\d+)/update/?$', ProductView.as_view(),
        name='product-update'),

    url(r'^product/(?P<pk>\d+)/delete/?$', DeleteProductView.as_view(),
        name='product-delete'),

    url(r'^peoples/?$', PeoplesView.as_view(), name='people-list'),

    url(r'^people/add/?$', PeopleCreateView.as_view(), name='people-new'),

    url(r'^people/(?P<pk>\d+)/update/?$', PeopleView.as_view(),
        name='people-update'),
    url(r'^people/(?P<pk>\d+)/delete/?$', DeletePeopleView.as_view(),
        name='people-delete'),


    url(r'^contractors/?$', ContractorsView.as_view(), name='contractor-list'),

    url(r'^contractor/add/?$', ContractorCreateView.as_view(),
        name='contractor-new'),

    url(r'^contractor/(?P<pk>\d+)/update/?$', ContractorView.as_view(),
        name='contractor-update'),

    url(r'^contractor/(?P<pk>\d+)/delete/?$', DeleteContractorView.as_view(),
        name='contractor-delete'),


    url(r'^menus/?$', MenuCalendarView.as_view(), name='menu-list'),

    url(r'^menu/(?P<year>\d{4})[.-]{1}(?P<month>\d{2})[.-]{1}(?P<day>\d{2})'
        '/create', MenuView.as_view(), {'create': True}, name='menus-new'),

    url(r'^menu/(?P<year>\d{4})[.-]{1}(?P<month>\d{2})[.-]{1}(?P<day>\d{2})'
        '/update', MenuView.as_view(), name='menu-update'),

    url(r'^menu/(?P<year>\d{4})[.-]{1}(?P<month>\d{2})[.-]{1}(?P<day>\d{2})'
        '/delete', delete_menu, name='menu-delete'),

    url(r'^menu/(?P<year>\d{4})[.-]{1}(?P<month>\d{2})[.-]{1}(?P<day>\d{2})/' +
        COPY_TO_MONTH + '/?$', copy_menu, {'copy': COPY_TO_MONTH},
        name='menus-' + COPY_TO_MONTH),
    url(r'^menu/(?P<year>\d{4})[.-]{1}(?P<month>\d{2})[.-]{1}(?P<day>\d{2})/' +
        COPY_TO_TOMORROW + '/?$', copy_menu, {'copy': COPY_TO_TOMORROW},
        name='menus-' + COPY_TO_TOMORROW),

    url(r'^json/yield_dish/(?P<dish>\d*)/(?P<csrfmiddlewaretoken>.+)',
        yield_dish, name='yield_dish'),
    url(r'^json/create_dish/(?P<name>.*)/(?P<csrfmiddlewaretoken>.+)',
        create_dish, name='create_dish'),
    url(r'^json/product/add/?$', create_product, name='json-product-new'),
    #url(r'^update_products/?$', update_products, name='jupdate_products'),
]
