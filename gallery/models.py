from django.db import models
from blog.images import compress, upload_to_gallery
from blog.models import gen_slug
# Create your models here.

class Gallery(models.Model):
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
            self.slug = gen_slug(self.title)
        if self.img:
            self.img = compress(self.img)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            object = Gallery.objects.get(id=self.id)
            object.img.delete()
        except (Gallery.DoesNotExist, ValueError):
            pass
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
