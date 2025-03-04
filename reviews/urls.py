from django.urls import path
from . import views

urlpatterns = [
    path('review/<int:product_id>/', views.leave_review, name='leave_review'),
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
]