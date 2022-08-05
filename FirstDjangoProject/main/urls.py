from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('reviews', views.reviews, name='reviews'),
    path('catalog', views.CatalogView.as_view(), name='catalog'),
    path('catalog/<str:category_name>/', views.ProductByCategoryView.as_view(), name='products_by_category'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('registration/', views.UserRegister.as_view(), name='registration'),
    path('login/', views.UserLogIn.as_view(), name='login'),
    path('logout/', views.UserLogOut.as_view(), name='logout'),
    path('account/profile/', views.UserChangeProfileView.as_view(), name='profile')

]
urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
