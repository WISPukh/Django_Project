from django.contrib import admin
from django.contrib.admin import ModelAdmin

from cart.models import OrderItem, Order


@admin.register(Order)
class AdminManageOrder(ModelAdmin):
    list_display = ('pk', 'quantity', 'total_price', 'city', 'address',)
    ordering = ('pk',)


@admin.register(OrderItem)
class AdminManageOrderItem(ModelAdmin):
    list_display = ('order_id', 'product_name', 'unit_price', 'quantity', 'customer_id')
    ordering = ('order_id',)
