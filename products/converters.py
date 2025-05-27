from django.urls import register_converter


class SlugConverter:
    regex = '[a-zA-Z0-9-]{1,20}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(SlugConverter, 'category_slug')
