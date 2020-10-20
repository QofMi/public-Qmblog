from django.contrib import admin
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.html import mark_safe

from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied


admin.site.site_title = 'QMBLOG'
admin.site.site_header = 'QMBLOG'


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    """
    Регистраци модели Post в административной части сайта
    """
    list_display = ['title', 'user', 'date_pub', 'get_img']
    exclude = ['slug']
    readonly_fields = ('get_img', 'user', 'date_pub',)

    def get_img(self, obj):
        """
        Отображение ихображения
        """
        return mark_safe(f'<img src={obj.img.url} width="200" height="auto">')

    get_img.short_description = 'Изображение'

    def get_form(self, request, obj=None, **kwargs):
        """
        Ограничение доступа к объектам модели Post
        """
        if obj is None:
            return super(AdminPost, self).get_form(request, obj, **kwargs)

        if request.user.groups.filter(name="Модераторы").exists():
            if obj.user != request.user:
                raise PermissionDenied
        return super(AdminPost, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Добавление пользователя при сохранении модели Post
        """
        if obj.user is None:
            obj.user = request.user
        return super(AdminPost, self).save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        """
        Запрет на удаление объектов модели Post
        """
        if request.user.groups.filter(name="Модераторы").exists():
            raise PermissionDenied
        return super(AdminPost, self).delete_model(request, queryset)


class AdminUser(UserAdmin):
    """
    Регистраци пользовательской модели User в административной части сайта
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login',)

    def change_view(self, request, *args, **kwargs):
        """
        Разграничение отображения контента для персонала и суперпользователя
        """
        if not request.user.is_superuser:
            self.readonly_fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'user_permissions', 'last_login', 'date_joined')
        return super(AdminUser, self).change_view(request, *args, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        """
        Включение статуса персонала при присваивании пользователю определенной группы
        """
        if obj.is_superuser:
            obj.is_staff = True
            obj.save()
        elif obj.groups.filter(name="Модераторы").exists() or obj.groups.filter(name="Администраторы").exists():
            obj.is_staff = True
            obj.save()
        else:
            obj.is_staff = False
            obj.save()
        return super(AdminUser, self).get_form(request, obj, **kwargs)


admin.site.unregister(User)
admin.site.register(User, AdminUser)
