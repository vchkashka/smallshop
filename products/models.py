from django.db import models


class Product(models.Model): 
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField()
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
