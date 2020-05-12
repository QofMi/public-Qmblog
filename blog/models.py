from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from .images import compress, upload_to

# Create your models here.

# Генерация slug и перевод из кириллицы в транслит
alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

def gen_slug(s):
    new_slug = slugify(''.join(alphabet.get(w, w) for w in s.lower()))
    return new_slug + '-' + str(int(time()))
#---------------------------------------------------------------------------------------

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=150, db_index=True)
    slug = models.SlugField('Идентификатор',max_length=150, blank=True, unique=True)
    img = models.ImageField('Изображение',upload_to=upload_to,  blank=True,)
    body = RichTextUploadingField('Текст', config_name='default', blank=True, null=True, db_index=True)
    date_pub = models.DateTimeField('Дата публикации', auto_now_add=True)
    user = models.ForeignKey( User, on_delete=models.SET_NULL, verbose_name='Пользователь', blank=True, null=True)

    class Meta:
         ordering = ['-date_pub',]
         verbose_name = 'Посты'
         verbose_name_plural = "Посты"

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            object = Post.objects.get(id=self.id)
            object.img.delete()
        except (Post.DoesNotExist, ValueError):
            pass
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
