import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


def validate_russian_phone(value):
    if not re.fullmatch(r"\+7\d{10}", value):
        raise ValidationError(
            _("Введите номер в формате +7XXXXXXXXXX (10 цифр после +7)")
        )


class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True,
                              null=True, verbose_name="Фотография")
    phone = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        validators=[validate_russian_phone]
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class SellerReview(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_written'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв о продавце'
        verbose_name_plural = 'Отзывы о продавцах'

    def __str__(self):
        return f"{self.reviewer.username} → {self.seller.username}"
