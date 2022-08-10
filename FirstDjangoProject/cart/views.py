from django.shortcuts import render, get_object_or_404, redirect

from django.views.decorators.http import require_POST

from main.models import Product
from main.views import menu
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add_to_cart(product=product,
                         quantity=cd['quantity'],
                         update_quantity=cd['update'])
    return redirect('product_detail', pk)


def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'main/cart_detail.html', context={'cart': cart, 'menu': menu})
