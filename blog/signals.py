from .models import Post
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from .signals_services import _compressing_image_signal, _delete_image_signal


@receiver(pre_save, sender=Post)
def compressing_image_post_signal(sender, instance, **kwargs):
    """
    Сигнал сжатия изображений модели Post
    """
    _compressing_image_signal(instance, model=sender)


@receiver(pre_delete, sender=Post)
def delete_image_post_signal(sender, instance, **kwargs):
    """
    Сигнал удаления изображений модели Post
    """
    _delete_image_signal(instance, model=sender)
