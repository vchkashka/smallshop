from django.shortcuts import render
from products.views import data_db


menu = [{'title': "О сайте", 'url_name': 'about_us'},
        {'title': "Обратная связь", 'url_name':
         'contact'},
        {'title': "Войти", 'url_name': 'login'},
        ]


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'products': data_db,
    }
    return render(request, 'core/index.html', data)


def about_us(request):
    data = {
        'title': 'О нас',
        'menu': menu,
        }
    return render(request, 'core/about.html', data)


def contact(request):
    data = {
        'title': 'Контактная информация',
        'menu': menu,
        }
    return render(request, 'core/contact.html', data)
