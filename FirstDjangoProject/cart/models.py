from django.db import models
from django.utils.translation import gettext_lazy as _

from shop.models import Product
from users.models import User


class OrderStatus(models.TextChoices):
    CART = 'CART', _('Cart')
    CREATED = 'CREATED', _('Created')
    PAID = 'PAID', _('Paid')
    IS_DELIVERING = 'IS_DELIVERING', _('Is Delivering')
    DELIVERED = 'DELIVERED', _('Delivered')


class OrderItem(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    product_id = models.ForeignKey(Product, on_delete=models.NOT_PROVIDED)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))
    product_name = models.CharField(default=0, max_length=50, verbose_name=_('Product name'))
    unit_price = models.IntegerField(default=0, verbose_name=_('Price'))

    class Meta:
        verbose_name = _('Item in order')
        verbose_name_plural = _('Items in order')


class Order(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Customer'))
    total_price = models.IntegerField(default=0, verbose_name=_('Order price'))
    product = models.ManyToManyField(Product)
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))
    city = models.CharField(max_length=80, verbose_name=_('City'), default='')
    address = models.CharField(max_length=150, verbose_name=_('Address'), default='')
    status = models.CharField(max_length=13, choices=OrderStatus.choices, default=OrderStatus.CART)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{_("Order")} №{self.pk}'
