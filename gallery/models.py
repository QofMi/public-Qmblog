from django.db import models
from blog.images import _compressing_image, upload_to_gallery
from blog.utils import _gen_slug


class Gallery(models.Model):
    """
    Модель изображений в галереи
    """
    title = models.CharField('Заголовок', max_length=150, db_index=True)
    slug = models.SlugField('Идентификатор',max_length=150, blank=True, unique=True)
    img = models.ImageField('Изображение',upload_to=upload_to_gallery,)
    date_pub = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
         ordering = ['-date_pub',]
         verbose_name = 'Галерея'
         verbose_name_plural = "Галерея"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = _gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
