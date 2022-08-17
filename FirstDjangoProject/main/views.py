from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import generic

from cart.forms import CartAddProductForm
from .models import *


def index(request):
    return render(request, 'main/home.html')


def about(request):
    return render(request, 'main/about.html')


def reviews(request):
    return render(request, 'main/reviews.html')


class CatalogView(generic.ListView):
    model = Category
    ordering = 'id'
    template_name = 'main/catalog.html'
    context_object_name = 'catalog_list'


class ProductByCategoryView(generic.ListView):
    model = Product
    context_object_name = 'products_list'
    template_name = 'main/products_by_category.html'

    def get_queryset(self):
        return Product.objects.filter(category__name=self.kwargs.get('category_name'))


class ProductDetailView(generic.DetailView):
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
