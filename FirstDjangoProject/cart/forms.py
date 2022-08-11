from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)


class CartDeleteProductForm(forms.Form):
    delete_product_pk = forms.IntegerField(widget=forms.HiddenInput)
