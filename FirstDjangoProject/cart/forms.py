from django import forms
from django.utils.translation import gettext_lazy as _

from cart.models import Order

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=_('Quantity'))


class MakeOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('city', 'address')
