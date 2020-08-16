from django.shortcuts import render
from .utils import _get_client_ip
from .models import *
from django.utils import timezone
from django.contrib import messages


def _add_ip_to_temporary_ban_ip_list(request):
    """
    Добавляет ip адрес пользователя в список временно заблокированных ip адресов
    """
    object, created = TemporaryBanIp.objects.get_or_create(
    defaults={
    'ip_address': _get_client_ip(request),
    'time_unblock': timezone.now()
    },
    ip_address=_get_client_ip(request))
    return object


def _check_status_temporary_ban_ip(request, object, template, context):
    """
    Проверка статуса блокировки
    """
    if object.status is True and object.time_unblock > timezone.now():
        if object.attempts == 3 or object.attempts == 6:
            messages.add_message(request, messages.ERROR, 'Попытки входа ограничены на 15 минут')
            context['has_error']=True
        elif object.attempts == 9:
            messages.add_message(request, messages.ERROR, 'Попытки входа ограничены на 24 часа')
            context['has_error']=True
    elif object.status is True and object.time_unblock < timezone.now():
        object.status = False
        object.save()


def _count_errors_for_temporary_ban_ip(object):
    """
    Подсчсет неудачных попыток входа и присваивание статуса блокировки объекту
    """
    object.attempts += 1
    if object.attempts == 3 or object.attempts == 6:
        object.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
        object.status = True
    elif object.attempts == 9:
        object.time_unblock = timezone.now() + timezone.timedelta(1)
        object.status = True
    elif object.attempts > 9:
        object.attempts = 1
    object.save()
