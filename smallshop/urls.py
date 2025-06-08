from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from .views import page_not_found
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "Панель администрирования"
admin.site.index_title = ("Магазин изделий ручной работы и винтажных "
                          "вещей 'Лавка редкостей'")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls', namespace="users")),
    path('products/', include('products.urls')),
]

handler404 = page_not_found

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
