from django import forms
from .models import Category, TagProduct, Product, CategoryDetails
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


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="Категория не выбрана",
                                      label="Категория")
    tags = forms.ModelMultipleChoiceField(queryset=TagProduct.objects.all(),
                                          required=False,
                                          widget=forms.CheckboxSelectMultiple,
                                          label="Теги")

    class Meta:
        model = Product
        fields = ['title', 'content', 'price', 'image', 'is_published',
                  'category', 'tags']
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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class CategoryDetailsForm(forms.ModelForm):
    class Meta:
        model = CategoryDetails
        fields = ['description', 'banner_image']
