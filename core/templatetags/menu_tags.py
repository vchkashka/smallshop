from django import template

register = template.Library()


@register.inclusion_tag('core/menu.html')
def show_menu():
    menu = [
        {'title': "О сайте", 'url_name': 'about_us'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
    ]
    return {'menu': menu}
