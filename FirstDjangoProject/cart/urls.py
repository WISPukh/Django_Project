from django.urls import path
from .views import (AddCartItemView, CartView, RemoveCartItemView)

urlpatterns = [
    path('<int:pk>/', CartView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', AddCartItemView.as_view(), name='cart_add'),
    path('remove_<int:pk>/', RemoveCartItemView.as_view(), name='cart_remove'),

]
