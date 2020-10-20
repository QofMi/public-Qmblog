from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.core.exceptions import PermissionDenied


@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    """
    Запрет на удаление суперпользователя
    """
    if instance.is_superuser:
        raise PermissionDenied
