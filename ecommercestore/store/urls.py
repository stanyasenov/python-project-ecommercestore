from django.urls import path

from . import views
from .views import HomeView, ProductDetailView, \
    EditProductView, DeleteProductView, AddProductView
from ..accounts.views import ProfileDetailsView

urlpatterns = [
    path('', HomeView, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('add_product/', AddProductView.as_view(), name="product add"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="product details"),
    path('edit/product/<int:pk>/', EditProductView.as_view(), name="product edit"),
    path('delete/product/<int:pk>/', DeleteProductView.as_view(), name="product delete"),
    path('process_order/', views.processOrder, name="process_order"),



]