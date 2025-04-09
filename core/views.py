from django.shortcuts import render
from products.models import Product


def index(request):
    products = Product.published.all()
    data = {
        'title': 'Главная страница',
        'products': products,
        'cat_selected': 0,
    }
    return render(request, 'core/index.html', data)


def about_us(request):
    data = {
        'title': 'О нас',
        }
    return render(request, 'core/about.html', data)


def contact(request):
    data = {
        'title': 'Контактная информация',
        }
    return render(request, 'core/contact.html', data)
