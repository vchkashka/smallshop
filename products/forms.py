from django import forms
from .models import Category, TagProduct, Product
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = ("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ"
                     "абвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- ")
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else ("Должны присутствовать "
                                                "только русские символы, "
                                                "дефис и пробел.")

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


# class AddProductForm(forms.Form):
#     title = forms.CharField(max_length=255, label="Название",
#                             validators=[RussianValidator(), ])
#     content = forms.CharField(widget=forms.Textarea(), required=False,
#                               label="Описание")
#     price = forms.DecimalField(max_digits=10, decimal_places=2, label="Цена")
#     # image = forms.ImageField(label="Изображение")
#     is_published = forms.BooleanField(label="Статус", required=False)
#     slug = forms.SlugField(max_length=255, label="URL")

#     category = forms.ModelChoiceField(queryset=Category.objects.all(),
#                                       label="Категория",
#                                       empty_label="Категория не выбрана")
#     tags = forms.ModelChoiceField(queryset=TagProduct.objects.all(),
#                                   required=False, label="Теги",
#                                   empty_label="Без тегов")

class AddProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="Категория не выбрана",
                                      label="Категория")
    tags = forms.ModelMultipleChoiceField(queryset=TagProduct.objects.all(),
                                          required=False,
                                          widget=forms.CheckboxSelectMultiple,
                                          label="Теги")

    class Meta:
        model = Product
        fields = ['title', 'content', 'price', 'is_published', 'slug',
                  'category', 'tags', 'image']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price
