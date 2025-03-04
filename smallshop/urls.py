from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from .views import page_not_found


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls')),
    path('reviews/', include('reviews.urls')),
]

handler404 = page_not_found
