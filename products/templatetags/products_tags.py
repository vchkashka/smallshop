from django import template
import products.views as views

register = template.Library()


@register.inclusion_tag('products/list.html')
def show_categories(cat_selected=0):
    categories = views.categories_db
    return {"categories": categories, 'cat_selected': cat_selected}
