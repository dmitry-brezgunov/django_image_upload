from django.contrib import admin

from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "original_image", "url", "resized_image", )


admin.site.register(Image, ImageAdmin)
