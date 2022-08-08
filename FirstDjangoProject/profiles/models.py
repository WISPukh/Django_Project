from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator


# Модель Profile, которая хранит всевозможную информацию о пользователе для отображения на странице.
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    bio = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='О себе'
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name='День рождения'
    )
    phone = models.CharField(
        validators=[RegexValidator(r'\d{11}', 'Enter a valid phone number. Minimum 11 digits', code='invalid')],
        max_length=11,
        null=True,
        blank=True,
        verbose_name='Номер телефона'
    )
    age = models.IntegerField(
        # validators=[RegexValidator(r"\d+", 'Enter a valid age', code='invalid')],  не ебу пока не получается сделать
        null=True,
        blank=True,
        verbose_name='Возраст'
    )
    region = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Область'
    )

    def __str__(self):
        return str(self.pk)  # TODO: сделать по нормальному вывод email
