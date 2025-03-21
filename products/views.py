from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Product


categories_db = [
    {'id': 1, 'name': 'Украшения', 'slug': 'jewerly'},
    {'id': 2, 'name': 'Винтаж', 'slug': 'vintage'},
    {'id': 3, 'name': 'Новый год', 'slug': 'newYear'},
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
    filtered_products = Product.objects.all().filter(title__contains=query)

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
