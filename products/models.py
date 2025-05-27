from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from django.db import models

User = get_user_model()


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=Product.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name="Загловок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name="Слаг")

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
         'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
         'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
         'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y',
         'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class Product(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Скрыто'
        PUBLISHED = 1, 'Опубликовано'

    objects = models.Manager()
    published = PublishedModel()
    title = models.CharField(max_length=255, verbose_name="Название")
    content = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                blank=False, null=False, verbose_name="Цена")
    image = models.ImageField(upload_to="product_images/",
                              verbose_name="Изображение")
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT, verbose_name="Состояние")
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name="Категория")
    tags = models.ManyToManyField('TagProduct', blank=True,
                                  related_name='tags', verbose_name="Теги")
    seller = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name='products', null=True,
                               default=None)
    favorites = models.ManyToManyField(User, related_name='favorite_products', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs):
        translit_title = translit_to_eng(self.title)
        self.slug = slugify(translit_title)
        super().save(*args, **kwargs)


class TagProduct(models.Model):
    tag = models.CharField(max_length=100, db_index=True,
                           verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name="Слаг")

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тег товара'
        verbose_name_plural = 'Теги товара'


class CategoryDetails(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE,
                                    related_name='details')
    description = models.TextField(blank=True, verbose_name="Описание")
    banner_image = models.ImageField()

    def __str__(self):
        return self.category.name

    class Meta:
        verbose_name = 'Описание категории'
        verbose_name_plural = 'Описания категорий'
