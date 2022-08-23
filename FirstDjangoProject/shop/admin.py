from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *

admin.site.register(Category)


class AdminManageProduct(ModelAdmin):
    search_fields = ('name',)
    ordering = ('price',)
    fieldsets = None

    @staticmethod
    def set_connections(form, c_type, category):
        form.base_fields['content_type'].initial = c_type
        form.base_fields['content_type'].disabled = True
        form.base_fields['content_type'].widget.can_add_related = False
        form.base_fields['content_type'].widget.can_change_related = False

        form.base_fields['category'].initial = category
        form.base_fields['category'].widget.widget.allow_multiple_selected = False
        form.base_fields['category'].widget.can_add_related = False


@admin.register(Blender)
class AdminManageBlender(AdminManageProduct):
    model = Blender
    list_display = ('name', 'price', 'in_stock', 'description', 'volume', 'fan_speed')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        self.set_connections(form, '9', '3')
        return form


@admin.register(Combine)
class AdminManageCombine(AdminManageProduct):
    model = Combine
    list_display = ('name', 'price', 'in_stock', 'description', 'volume', 'max_power')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        self.set_connections(form, '10', '4')
        return form


@admin.register(Fridge)
class AdminManageFridge(AdminManageProduct):
    model = Fridge
    list_display = ('name', 'price', 'in_stock', 'description', 'height', 'width', 'length')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        self.set_connections(form, '11', '5')
        return form


@admin.register(Mixer)
class AdminManageMixer(AdminManageProduct):
    model = Mixer
    list_display = ('name', 'price', 'in_stock', 'description', 'mixer_type', 'fan_speed', 'bowl_size')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        self.set_connections(form, '12', '1')
        return form


@admin.register(Panel)
class AdminManagePanel(AdminManageProduct):
    model = Panel
    list_display = ('name', 'price', 'in_stock', 'description', 'height', 'width', 'length')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        self.set_connections(form, '13', '6')
        return form


@admin.register(Teapot)
class AdminManageTeapot(AdminManageProduct):
    model = Teapot
    list_display = ('name', 'price', 'in_stock', 'description', 'volume', 'max_power')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        self.set_connections(form, '14', '2')
        return form
