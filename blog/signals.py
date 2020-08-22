from .models import Post
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from .images import _compressing_image


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


def _compressing_image_signal(instance, model) -> None:
    """
    Сигнал сжатия изображений
    """
    if instance.img:
        try:
            objects = model.objects.get(slug__iexact=instance.slug)
            if instance.img != objects.img:
                objects.img.delete()
                instance.img = _compressing_image(instance.img)
        except:
            instance.img = _compressing_image(instance.img)


def _delete_image_signal(instance, model) -> None:
    """
    Сигнал удаления изображений
    """
    try:
        object = model.objects.get(slug__iexact=instance.slug)
        object.img.delete()
    except (model.DoesNotExist, ValueError):
        pass
