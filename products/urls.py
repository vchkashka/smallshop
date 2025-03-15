from django.urls import path
from . import views, converters


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.product_search, name='product_search'),
    path('category/<category_slug:category_slug>/', views.category_detail,
         name='category_detail'),
]
