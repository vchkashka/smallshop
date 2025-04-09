from django.urls import reverse
from django.db import models


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=Product.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Скрыто'
        PUBLISHED = 1, 'Опубликовано'

    objects = models.Manager()
    published = PublishedModel()
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                blank=False, null=False)
    image = models.ImageField()
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField('TagProduct', blank=True,
                                  related_name='tags')

    def __str__(self):
        return self.title


class TagProduct(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class CategoryDetails(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE,
                                    related_name='details')
    description = models.TextField(blank=True)
    banner_image = models.ImageField()

    def __str__(self):
        return self.category.name
