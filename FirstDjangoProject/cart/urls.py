from django.urls import path
from .views import (AddCartItemView, CartView)

urlpatterns = [
    path('<int:pk>/', CartView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', AddCartItemView.as_view(), name='cart_add'),
    # path('remove/<int:pk>', cart_remove, name='cart_remove'),
]
