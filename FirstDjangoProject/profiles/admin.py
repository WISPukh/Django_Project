from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Profile


@admin.register(Profile)
class AdminManageProfile(ModelAdmin):
    list_display = ('user', 'bio', 'birthday', 'phone', 'age', 'region')
    ordering = ('pk',)
