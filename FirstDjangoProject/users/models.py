from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


# Модель User, которая отвечает только за аутентификацию и авторизацию пользователя в системе.
class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), blank=False, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
