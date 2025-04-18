from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from .views import page_not_found


admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Магазин изделий ручной работы и винтажных вещей 'Лавка редкостей'"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
]


handler404 = page_not_found
