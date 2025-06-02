from django.urls import path
from . import views, converters


urlpatterns = [
    path('add/', views.AddProduct.as_view(), name='add_product'),
    path('edit/<slug:slug>/', views.UpdateProduct.as_view(),
         name='edit_product'),
    path('delete/<slug:slug>/', views.DeleteProduct.as_view(),
         name='delete_product'),

    path('search/', views.ProductSearchView.as_view(), name='product_search'),
    path('favorites/', views.favorite_products, name='favorite_products'),

    path('category/<category_slug:category_slug>/',
         views.ProductCategory.as_view(),
         name='category'),

    path('manage-categories/', views.manage_categories,
         name='manage_categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:pk>/', views.delete_category,
         name='delete_category'),
    path('add-tag/', views.add_tag, name='add_tag'),
    path('edit-tag/<int:pk>/', views.edit_tag, name='edit_tag'),
    path('delete-tag/<int:pk>/', views.delete_tag, name='delete_tag'),

    path('tag/<slug:tag_slug>/', views.TagProductList.as_view(), name='tag'),

    path('<slug:product_slug>/add-to-favorites/',
         views.add_to_favorites, name='add_to_favorites'),
    path('<slug:product_slug>/remove-from-favorites/',
         views.remove_from_favorites, name='remove_from_favorites'),

    path('<slug:product_slug>/', views.ShowProduct.as_view(),
         name='product_detail'),


]
