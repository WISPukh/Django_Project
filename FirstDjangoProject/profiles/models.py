from django.conf import settings
from django.db import models

from users.models import User


# Модель Profile, которая хранит всевозможную информацию о пользователе для отображения на странице.
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    bio = models.CharField(
        max_length=160,
        null=True,
        blank=True
    )
    birthday = models.DateField(
        null=True,
        blank=True
    )
    phone = models.IntegerField(
        null=True,
        blank=True
    )
    age = models.IntegerField(
        null=True,
    )
    region = models.IntegerField(
        null=True,
    )

    def __str__(self):
        return str(self.user)
