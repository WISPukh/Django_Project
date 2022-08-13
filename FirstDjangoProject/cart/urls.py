from django.urls import path
from .views import (
    AddCartItemView,
    CartView,
    RemoveCartItemView,
    MakeOrderView,
    OrderDetailView
)

urlpatterns = [
    path('<int:pk>/', CartView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', AddCartItemView.as_view(), name='cart_add'),
    path('remove_<int:pk>/', RemoveCartItemView.as_view(), name='cart_remove'),
    path('make_order/<int:pk>/', MakeOrderView.as_view(), name='make_order'),
    path('order_finished/<int:pk>/', OrderDetailView.as_view(), name='order_finished')
]
