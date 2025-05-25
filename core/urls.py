from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.AboutUs.as_view(), name='about_us'),
    path('contact/', views.Contact.as_view(), name='contact'),
]
