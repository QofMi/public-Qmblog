from django.contrib import admin
from .models import Gallery
from django.utils.html import mark_safe

# Register your models here.

@admin.register(Gallery)
class AdminGallery(admin.ModelAdmin):
    list_display = ['title', 'date_pub', 'get_img']
    exclude = ['slug']
    readonly_fields = ('get_img', 'date_pub',)
    def get_img(self, obj):
        return mark_safe(f'<img src={obj.img.url} width="200" height="auto">')

    get_img.short_description = 'Изображение'
