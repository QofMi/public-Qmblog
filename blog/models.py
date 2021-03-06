from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from .images import GenFilename
from .utils import _gen_slug


class Post(models.Model):
    """
    Модель записи в блоге
    """
    title = models.CharField('Заголовок', max_length=150, db_index=True)
    slug = models.SlugField('Идентификатор',max_length=150, blank=True, unique=True)
    img = models.ImageField('Изображение',upload_to=GenFilename('post'),  blank=True,)
    body = RichTextUploadingField('Текст', config_name='default', blank=True, null=True)
    date_pub = models.DateTimeField('Дата публикации', auto_now_add=True)
    user = models.ForeignKey( User, on_delete=models.SET_NULL, verbose_name='Пользователь', blank=True, null=True)

    class Meta:
         ordering = ['-date_pub',]
         verbose_name = 'Посты'
         verbose_name_plural = "Посты"

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = _gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
