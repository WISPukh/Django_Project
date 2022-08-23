from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

urlpatterns = i18n_patterns(
    path('', include('shop.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('users.urls')),
    path('cart/', include('cart.urls'))
)
