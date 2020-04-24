from django.contrib import admin
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.html import mark_safe


from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
# Register your models here.

admin.site.site_title = 'QMBLOG'
admin.site.site_header = 'QMBLOG'

#-------------------------------------------------------------------------------

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['title', 'user', 'date_pub', 'get_img']
    exclude = ['slug']
    def get_img(self, obj):
        return mark_safe(f'<img src={obj.img.url} width="200" height="auto">')

    def change_view(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.readonly_fields = ('get_img', 'user', 'date_pub',)
            return super(AdminPost, self).change_view(request, *args, **kwargs)

        elif request.user.groups.filter(name="Администраторы").exists():
            self.readonly_fields = ('get_img', 'user', 'date_pub',)
            return super(AdminPost, self).change_view(request, *args, **kwargs)
        else:
            self.readonly_fields =  ('title', 'img', 'body', 'get_img', 'user', 'date_pub',)
            return super(AdminPost, self).change_view(request, *args, **kwargs)

    get_img.short_description = 'Изображение'
#-------------------------------------------------------------------------------


# Разграничение отображения контента для персонала и суперпользователя при изменении польвателя
class AdminUser(UserAdmin):
    staff_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Персональная информация'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Права доступа'), {
            'fields': ('is_staff','groups',),
        }),
        (('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login',)
    def change_view(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            try:
                self.fieldsets = self.staff_fieldsets
                self.readonly_fields = ('username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_staff')
                response = super(AdminUser, self).change_view(request, *args, **kwargs)
            finally:
                self.fieldsets = UserAdmin.fieldsets
                self.readonly_fields = ('last_login', 'date_joined',)
            return response
        else:
            return super(AdminUser, self).change_view(request, *args, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        if obj.is_superuser:
            obj.is_staff = True
            obj.save()
        elif obj.groups.filter(name="Модераторы").exists() or obj.groups.filter(name="Администраторы").exists():
            obj.is_staff = True
            obj.save()
        else:
            obj.is_staff = False
            obj.save()
        return super().get_form(request, obj, **defaults)


admin.site.unregister(User)
admin.site.register(User, AdminUser)

#-------------------------------------------------------------------------------

# Запрет на удаление суперпользователя
@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    if instance.is_superuser:
        raise PermissionDenied
