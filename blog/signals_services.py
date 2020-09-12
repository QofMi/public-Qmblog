from .images import _compressing_image


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
        except (model.DoesNotExist, ValueError):
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
