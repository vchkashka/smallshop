from django.shortcuts import render
from django.http import HttpResponse

def cart_view(request):
    return HttpResponse("Корзина")

def add_to_cart(request, product_id):
    return HttpResponse("Добавить товар в корзину")

def remove_from_cart(request, product_id):
    return HttpResponse("Удалить товар из корзины")
