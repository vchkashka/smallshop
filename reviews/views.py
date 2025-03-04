from django.shortcuts import render
from django.http import HttpResponse


def leave_review(request, product_id):
    return HttpResponse("Оставить отзыв")


def product_reviews(request, product_id):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"Отзывы на товар №{product_id}")
