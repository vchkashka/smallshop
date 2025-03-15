from django import template
import core.views as views

register = template.Library()


@register.simple_tag()
def get_categories():
    return views.cats_db


# @register.inclusion_tag()
# def show_categories():
#     cats = views.cats_db
#     return {"cats": cats}
