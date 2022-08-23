from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from users.models import User


class Product(models.Model):
    name = models.CharField(_('Product name'), max_length=50)
    description = models.CharField(max_length=250, verbose_name=_('Description'))
    price = models.IntegerField(default=0, verbose_name=_('Price'))
    in_stock = models.IntegerField(default=0, verbose_name=_('In stock'))
    category = models.ManyToManyField('Category')
    img = models.ImageField(upload_to='uploads/')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=50)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


class Mixer(Product):
    mixer_type = models.CharField(max_length=50, verbose_name=_('Mixer type'))
    fan_speed = models.IntegerField(default=1000, verbose_name=_('Fan speed'))
    bowl_size = models.IntegerField(default=5, verbose_name=_('Bowl size'))

    class Meta:
        verbose_name = _('Mixer')
        verbose_name_plural = _('Mixers')


class Teapot(Product):
    volume = models.IntegerField(default=2, verbose_name=_('Volume'))
    max_power = models.IntegerField(default=70, verbose_name=_('Power'))

    class Meta:
        verbose_name = _('Teapot')
        verbose_name_plural = _('Teapots')


class Blender(Product):
    volume = models.IntegerField(default=1, verbose_name=_('Volume'))
    fan_speed = models.IntegerField(default=500, verbose_name=_('Fan speed'))

    class Meta:
        verbose_name = _('Blender')
        verbose_name_plural = _('Blenders')


class Combine(Product):
    volume = models.IntegerField(default=2, verbose_name=_('Volume'))
    max_power = models.IntegerField(default=50, verbose_name=_('Power'))

    class Meta:
        verbose_name = _('Combine')
        verbose_name_plural = _('Combines')


class Fridge(Product):
    height = models.IntegerField(default=100, verbose_name=_('Height'))
    width = models.IntegerField(default=50, verbose_name=_('Width'))
    length = models.IntegerField(default=60, verbose_name=_('Length'))

    class Meta:
        verbose_name = _('Fridge')
        verbose_name_plural = _('Fridges')


# варочные панели, ну наверное типа печки
class Panel(Product):
    height = models.IntegerField(default=100, verbose_name=_('Height'))
    width = models.IntegerField(default=50, verbose_name=_('Width'))
    length = models.IntegerField(default=60, verbose_name=_('Length'))

    class Meta:
        verbose_name = _('Panel')
        verbose_name_plural = _('Panels')


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Category name'))
    img_url = models.ImageField(max_length=50, upload_to='category_images/')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products_by_category', args=[str(self.name)])
