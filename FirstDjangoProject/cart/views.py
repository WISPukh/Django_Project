from django.db.models import F
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView

from main.models import Cart
from .forms import CartAddProductForm


class CartView(ListView):
    template_name = 'main/cart_detail.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(customer_id_id=self.kwargs.get('pk'))


class AddCartItemView(CreateView):
    model = Cart

    def post(self, request, *args, **kwargs):
        form = CartAddProductForm(request.POST)
        user_pk = request.session['_auth_user_id']
        product_pk = self.kwargs.get('pk')
        quantity = form.data['quantity']

        order_item, created_order_item = Cart.objects.get_or_create(
            customer_id_id=user_pk,
            product_id_id=product_pk
        )
        if created_order_item:
            order_item.quantity = quantity
        else:
            order_item.quantity = F('quantity') + quantity
        order_item.save()
        return redirect('product_detail', product_pk)
