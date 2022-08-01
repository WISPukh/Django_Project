from django.shortcuts import render
from django.views import generic
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
        current_item = Product.objects.get(pk=self.kwargs.get('pk'))
        # print(ContentType.model_class(current_item.content_type))
        content_type = ContentType.model_class(current_item.content_type)
        return content_type.objects.all()
