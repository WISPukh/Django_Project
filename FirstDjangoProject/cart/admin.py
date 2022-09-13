from django.utils.translation import gettext_lazy as _
from django.contrib.admin import (
    ModelAdmin,
    TabularInline,
    register,
    display,
    action,
)

from cart.models import OrderItem, Order


class OrderItemsInline(TabularInline):
    model = OrderItem
    fk_name = 'order_id'
    extra = 0
    exclude = ('product_name',)


@register(Order)
class AdminManageOrder(ModelAdmin):
    list_display = (
        '__str__',
        'customer_id',
        'quantity',
        'total_price',
        'status',
        'city',
        'address',
        'show_full_address',
    )
    list_editable = ('status',)
    ordering = ('id',)
    actions = ('change_status',)
    exclude = ('product',)
    inlines = [
        OrderItemsInline,
    ]

    @display(description=_('Full address'))
    def show_full_address(self, obj):
        return ', '.join([obj.city, obj.address])

    @action(description=_('Mark delivered'))
    def change_status(self, request, queryset):  # noqa
        queryset.update(status='DELIVERED')
