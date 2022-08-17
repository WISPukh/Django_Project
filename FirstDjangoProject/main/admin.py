from django.contrib import admin
from .models import *
from profiles.models import Profile


admin.site.register(Product)
admin.site.register(Profile)

admin.site.register(Order)


admin.site.register(Combine)
admin.site.register(Mixer)
admin.site.register(Fridge)
admin.site.register(Blender)
admin.site.register(Teapot)
admin.site.register(Panel)

admin.site.register(Category)
