from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_POST

from .cart import Cart as RealCart
from .forms import CartAddProductForm
from .models import *

menu = [
    {'title': 'Главная', 'url': 'index', 'img_url': 'img/home.png'},
    {'title': 'О компании', 'url': 'about', 'img_url': 'img/about.png'},
    {'title': 'Каталог товаров', 'url': 'catalog', 'img_url': 'img/catalog.png'},
    {'title': 'Отзывы', 'url': 'reviews', 'img_url': 'img/review.png'},
]


def index(request):
    return render(request, 'main/home.html', {'menu': menu})


def about(request):
    return render(request, 'main/about.html', {'menu': menu})


def reviews(request):
    return render(request, 'main/reviews.html', {'menu': menu})


class DataMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class CatalogView(DataMixin, generic.ListView):
    model = Category
    ordering = 'id'
    template_name = 'main/catalog.html'
    context_object_name = 'catalog_list'


class ProductByCategoryView(DataMixin, generic.ListView):
    model = Product
    context_object_name = 'products_list'
    template_name = 'main/products_by_category.html'

    def get_queryset(self):
        return Product.objects.filter(category__name=self.kwargs.get('category_name'))


class ProductDetailView(DataMixin, generic.DetailView):
    context_object_name = 'product_detail'
    template_name = 'main/product_detail.html'

    def get_queryset(self):
        current_item = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        content_type = ContentType.model_class(current_item.content_type)
        return content_type.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        cart_product_form = CartAddProductForm()
        context['cart_form'] = cart_product_form
        return context


@require_POST
def cart_add(request, pk):
    cart = RealCart(request)
    product = get_object_or_404(Product, pk=pk)
    form = CartAddProductForm(request.POST)
    print(product.in_stock)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add_to_cart(product=product,
                         quantity=cd['quantity'],
                         update_quantity=cd['update'])
    return redirect('product_detail', pk)


def cart_remove(request, pk):
    cart = RealCart(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = RealCart(request)
    return render(request, 'main/cart_detail.html', context={'cart': cart, 'menu': menu})
