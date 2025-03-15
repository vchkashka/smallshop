from django.shortcuts import render


menu = [{'title': "О сайте", 'url_name': 'about_us'},
        {'title': "Обратная связь", 'url_name':
         'contact'},
         {'title': "Список товаров", 'url_name':
         'product_list'},
        {'title': "Войти", 'url_name': 'login'},
        ]


data_db = [
    {'id': 1, 'title': 'Серьги из бисера', 'content':
     '', 'is_published': True},
    {'id': 2, 'title': 'Винтажная ваза', 'content':
     '', 'is_published': False},
    {'id': 3, 'title': 'Елочная игрушка', 'content':
     '', 'is_published': True},
]

categories_db = [
    {'id': 1, 'name': 'Украшения'},
    {'id': 2, 'name': 'Винтаж'},
    {'id': 3, 'name': 'Новый год'},
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
