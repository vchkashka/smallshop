from django.shortcuts import render
from django.http import HttpResponse, Http404


def create_order(request):
    return HttpResponse("Создание заказа")


def order_detail(request, order_id):
    if order_id < 1:
        raise Http404()
    return HttpResponse("Детали заказа")


def order_status(request, order_id):
    return HttpResponse("Статус заказа")
