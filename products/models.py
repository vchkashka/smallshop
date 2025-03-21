from django.db import models


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=Product.Status.PUBLISHED)


class Product(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Скрыто'
        PUBLISHED = 1, 'Опубликовано'

    objects = models.Manager()
    published = PublishedModel()

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField()
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    def __str__(self):
        return self.title
