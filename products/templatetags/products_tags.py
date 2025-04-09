from django import template
from django.db.models import Count
from products.models import Category, TagProduct

register = template.Library()


@register.inclusion_tag('products/list.html')
def show_categories(cat_selected=0):
    categories = Category.objects.annotate(
        total=Count("product")).filter(total__gt=0)
    return {"categories": categories, 'cat_selected': cat_selected}


@register.inclusion_tag('products/list_tags.html')
def show_all_tags():
    return {"tags": TagProduct.objects.annotate(
        total=Count("tags")).filter(total__gt=0)}
