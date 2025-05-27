from django.urls import path
from . import views, converters


urlpatterns = [
    path('addproduct/', views.AddProduct.as_view(), name='add_product'),
    path('edit/<slug:slug>/', views.UpdateProduct.as_view(),
         name='edit_product'),
    path('delete/<slug:slug>/', views.DeleteProduct.as_view(),
         name='delete_product'),
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
    path('favorites/', views.favorite_products, name='favorite_products'),
    path('category/<category_slug:category_slug>/',
         views.ProductCategory.as_view(),
         name='category'),
    path('<slug:product_slug>/add_to_favorites/',
         views.add_to_favorites, name='add_to_favorites'),
    path('<slug:product_slug>/remove_from_favorites/',
         views.remove_from_favorites, name='remove_from_favorites'),
    path('<slug:product_slug>/', views.ShowProduct.as_view(),
         name='product_detail'),
    path('tag/<slug:tag_slug>/', views.TagProductList.as_view(), name='tag'),
]
