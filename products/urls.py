from django.urls import path
from . import views, converters
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('addproduct/', views.addproduct, name='add_product'),
    path('search/', views.product_search, name='product_search'),
    path('', views.product_list, name='product_list'),
    path('category/<category_slug:category_slug>/', views.category_detail,
         name='category'),
    path('<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('tag/<slug:tag_slug>/', views.show_tag_productlist, name='tag'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
