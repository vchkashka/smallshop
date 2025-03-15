from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


categories_db = [
    {'id': 1, 'name': 'Украшения', 'slug': 'jewerly'},
    {'id': 2, 'name': 'Винтаж', 'slug': 'vintage'},
    {'id': 3, 'name': 'Новый год', 'slug': 'newYear'},
]

data_db = [
    {'id': 1, 'title': 'Серьги из бисера', 'content':
     'Изящное и стильное украшение, выполненное вручную. Они состоят из '
     'множества маленьких бусин, аккуратно сплетенных в оригинальный узор.',
     'is_published': True, 'image': 'product1.jpg'},
    {'id': 2, 'title': 'Винтажная ваза', 'content':
     '', 'is_published': False, 'image': ''},
    {'id': 3, 'title': 'Елочная игрушка', 'content':
     '', 'is_published': True, 'image': 'product3.jpg'},
    {'id': 4, 'title': 'Мыло ручной работы', 'content':
     '', 'is_published': True, 'image': 'product4.jpg'},
    {'id': 5, 'title': 'Карнавальная маска', 'content':
     '', 'is_published': True, 'image': 'product5.jpg'},
    {'id': 6, 'title': 'Заколка', 'content':
     '', 'is_published': True, 'image': 'product6.jpg'},
    {'id': 7, 'title': 'Кулон', 'content':
     '', 'is_published': True, 'image': 'product7.jpg'},
]


def product_list(request):
    return HttpResponse("Список товаров")


def product_detail(request, product_id):
    if product_id > 10:
        return redirect(reverse('home'))

    return HttpResponse(f"Товар №{product_id}")


def product_search(request):
    from core.views import menu
    query = request.GET.get('q', '').strip()  # Убираем лишние пробелы
    filtered_products = []

    if query:
        filtered_products = [p for p in data_db if query.lower() in
                             p['title'].lower()]

    data = {
        'title': 'Поиск товаров',
        'products': filtered_products,
        'query': query,
        'menu': menu,
    }
    return render(request, 'products/search.html', data)


def category_detail(request, category_slug):
    from core.views import menu

    category = next((c for c in categories_db if c["slug"] == category_slug),
                    None)
    if not category:
        return HttpResponse("Категория не найдена", status=404)

    cat_selected = category["id"]

    data = {
        'category': category,
        'cat_selected': cat_selected,
        'menu': menu,
    }
    return render(request, 'products/category_detail.html', data)
