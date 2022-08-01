from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('catalog', views.CatalogView.as_view(), name='catalog'),
    path('reviews', views.reviews, name='reviews'),
    path('catalog/<str:category_name>/', views.ProductByCategoryView.as_view(), name='products_by_category'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

]
