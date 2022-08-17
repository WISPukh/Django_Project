from django.urls import path
from .views import (
    AddCartItemView,
    CartView,
    RemoveCartItemView,
    MakeOrderView,
    OrdersView
)

urlpatterns = [
    path('', CartView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', AddCartItemView.as_view(), name='cart_add'),
    path('remove/<int:pk>/', RemoveCartItemView.as_view(), name='cart_remove'),
    path('make_order/', MakeOrderView.as_view(), name='make_order'),
    path('orders/', OrdersView.as_view(), name='orders')
]
