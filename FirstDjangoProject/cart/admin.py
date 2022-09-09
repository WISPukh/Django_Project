from django.contrib import admin
from django.contrib.admin import ModelAdmin

from cart.models import OrderItem, Order


@admin.register(Order)
class AdminManageOrder(ModelAdmin):
    list_display = ('pk', 'quantity', 'total_price', 'status', 'city', 'address', 'show_full_address',)
    ordering = ('pk',)

    @admin.display(description='Full address')
    def show_full_address(self, obj):
        return ', '.join([obj.city, obj.address])


@admin.register(OrderItem)
class AdminManageOrderItem(ModelAdmin):
    list_display = ('order_id', 'product_name', 'unit_price', 'quantity', 'customer_id')
    ordering = ('order_id',)
