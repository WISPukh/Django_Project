from django.urls import path
from .views import (cart_add, cart_detail, cart_remove)

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:pk>', cart_add, name='cart_add'),
    path('remove/<int:pk>', cart_remove, name='cart_remove'),
]
