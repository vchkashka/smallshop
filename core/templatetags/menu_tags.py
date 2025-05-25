from django import template

register = template.Library()


@register.inclusion_tag('core/menu.html', takes_context=True)
def show_menu(context):
    menu = [
        {'title': "О сайте", 'url_name': 'about_us'},
        {'title': "Обратная связь", 'url_name': 'contact'},
    ]
    return {
        'menu': menu,
        'user': context['user'],
    }
