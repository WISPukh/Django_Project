from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    index,
    about,
    reviews,
    CatalogView,
    ProductByCategoryView,
    ProductDetailView
)

urlpatterns = [
    path('', index, name='index'),
    path('about', about, name='about'),
    path('reviews', reviews, name='reviews'),
    path('catalog', CatalogView.as_view(), name='catalog'),
    path('catalog/<str:category_name>/', ProductByCategoryView.as_view(), name='products_by_category'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

]
urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
