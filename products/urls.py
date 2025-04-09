from django.urls import path
from . import views, converters


urlpatterns = [
    path('search/', views.product_search, name='product_search'),
    path('', views.product_list, name='product_list'),
    path('category/<category_slug:category_slug>/', views.category_detail,
         name='category'),
    path('<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('tag/<slug:tag_slug>/', views.show_tag_productlist, name='tag'),
]
