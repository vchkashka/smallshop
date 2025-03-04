from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Главная страница.")


def about_us(request):
    return HttpResponse("О нас.")


def contact(request):
    return HttpResponse("Контактная информация.")