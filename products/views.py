from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


def product_list(request):
    return HttpResponse("Список товаров")


def product_detail(request, product_id):
    if product_id > 10:
        return redirect(reverse('home'))

    return HttpResponse(f"Товар №{product_id}")


def product_search(request):
    return HttpResponse("Поиск товаров")


def category_detail(request, category_slug):
    return HttpResponse(f"Категория товаров - {category_slug}")
