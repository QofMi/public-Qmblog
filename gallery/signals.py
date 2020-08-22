from .models import Gallery
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from blog.signals import _compressing_image_signal, _delete_image_signal


@receiver(pre_save, sender=Gallery)
def compressing_image_gallery_signal(sender, instance, **kwargs):
    """
    Сигнал сжатия изображений модели Gallery
    """
    _compressing_image_signal(instance, model=sender)


@receiver(pre_delete, sender=Gallery)
def delete_image_gallery_signal(sender, instance, **kwargs):
    """
    Сигнал удаления изображений модели Gallery
    """
    _delete_image_signal(instance, model=sender)
