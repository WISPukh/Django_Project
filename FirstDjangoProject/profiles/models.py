from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# Модель Profile, которая хранит всевозможную информацию о пользователе для отображения на странице.
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    bio = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name=_("User's bio")
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Birthday')
    )
    phone = models.CharField(
        validators=[RegexValidator(r'\d{11}', 'Enter a valid phone number. Minimum 11 digits', code='invalid')],
        max_length=11,
        null=True,
        blank=True,
        verbose_name=_('Phone number')
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Age')
    )
    region = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('Region')
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return str(self.user)
