from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import generic

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
        # current_item = Product.objects.get(pk=self.kwargs.get('pk'))
        # print(ContentType.model_class(current_item.content_type))
        content_type = ContentType.model_class(current_item.content_type)
        return content_type.objects.all()
all