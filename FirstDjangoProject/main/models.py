import time

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from users.models import User


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=250, verbose_name='Описание')
    price = models.IntegerField(default=0, verbose_name='Цена')
    in_stock = models.IntegerField(default=0, verbose_name='В запасе')
    category = models.ManyToManyField('Category')
    img = models.ImageField(upload_to=f'uploads/')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


class Mixer(Product):
    mixer_type = models.CharField(max_length=50, verbose_name='Тип Миксера')
    fan_speed = models.IntegerField(default=1000, verbose_name='Скорость вентилятора')
    bowl_size = models.IntegerField(default=5, verbose_name='Размер чаши')


class Teapot(Product):
    volume = models.IntegerField(default=2, verbose_name='Объем')
    max_power = models.IntegerField(default=70, verbose_name='Мощность')


class Blender(Product):
    volume = models.IntegerField(default=1, verbose_name='Объем')
    fan_speed = models.IntegerField(default=500, verbose_name='Скорость вентилятора')


class Combine(Product):
    volume = models.IntegerField(default=2, verbose_name='Объем')
    max_power = models.IntegerField(default=50, verbose_name='Мощность')


class Fridge(Product):
    height = models.IntegerField(default=100, verbose_name='Высота')
    width = models.IntegerField(default=50, verbose_name='Ширина')
    length = models.IntegerField(default=60, verbose_name='Длина')


# варочные панели, ну наверное типа печки
class Panel(Product):
    height = models.IntegerField(default=100, verbose_name='Высота')
    width = models.IntegerField(default=50, verbose_name='Ширина')
    length = models.IntegerField(default=60, verbose_name='Длина')


# class Cart(models.Model):
#     customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)
#
#     def __str__(self):
#         return f'List of products of Customer {self.customer_id.email}'


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CART = 'CART', _('Cart')
        CREATED = 'CR', _('Created')
        PAID = 'PAID', _('Paid')
        IS_DELIVERING = 'IS_DEL', _('Is Delivering')
        DELIVERED = 'DEL', _('Delivered')

    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0, verbose_name='Цена заказа')
    product = models.ManyToManyField(Product)
    # product_name = models.CharField(max_length=50, verbose_name='Название товара', default=0)
    # unit_price = models.IntegerField(default=0, verbose_name='Цена')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    city = models.CharField(max_length=80, verbose_name='Город', default=f'{round(time.time())}')
    address = models.CharField(max_length=150, verbose_name='Адрес', default=f'{round(time.time())}')
    status = models.CharField(max_length=6, choices=OrderStatus.choices, default=OrderStatus.CART)

    def __str__(self):
        return f'Order of Customer {self.customer_id.email}'


class Category(models.Model):
    name = models.CharField(max_length=50)
    img_url = models.ImageField(max_length=50, upload_to='category_images/')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products_by_category', args=[str(self.name)])
