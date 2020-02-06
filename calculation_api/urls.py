from django.urls import path
from calculation_api.Views import views, MapView, UnitView, PeopleView, DishView, CalculationView, ProductView, \
    ContractorView, InvoiceView

urlpatterns = [
    path('auth/', views.AuthView.as_view()),
    path('map/', MapView.MapViewSet.as_view()),
    path('map/<int:id>', MapView.MapViewSet.as_view()),
    path('map_full/<int:id>', MapView.MapFullViewGet.as_view()),
    path('map_get/', MapView.MapViewGet.as_view()),
    path('select2/map/', MapView.MapSelectGet.as_view()),

    path('unit/', UnitView.UnitViewGet.as_view()),
    path('select2/unit/', UnitView.UnitSelectGet.as_view()),

    path('people/', PeopleView.PeopleViewSet.as_view()),

    path('dish/', DishView.DishViewSet.as_view()),
    path('dish/<int:id>', DishView.DishViewSet.as_view()),
    path('select2/dish/', DishView.DishSelect2Get.as_view()),
    path('dish_get/', DishView.DishViewSetGet.as_view()),

    # path('product_get/', ProductView.ProductViewGet.as_view()),
    path('select2/product/', ProductView.ProductSelect2Get.as_view()),
    path('product/', ProductView.ProductViewGet.as_view()),
    path('product/<int:id>', ProductView.ProductViewGet.as_view()),

    path('calculation/', CalculationView.CalculationViewSet.as_view()),
    path('contractor_get/', ContractorView.ContractorViewGet.as_view()),
    path('invoice_get/', InvoiceView.InvoiceViewGet.as_view()),
    path('invoice_items_get/', InvoiceView.InvoiceItemsViewGet.as_view()),
]
