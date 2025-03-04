from django.shortcuts import render
from django.http import HttpResponse


def register(request):
    return HttpResponse("Регистрация")


def login_view(request):
    return HttpResponse("Вход")


def profile(request):
    return HttpResponse("Профиль")


def logout_view(request):
    return HttpResponse("Выход")
