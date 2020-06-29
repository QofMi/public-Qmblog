from django.db import models


class TemporaryBanIp(models.Model):
    """
    Модель временно заблокированных ip адресов при неудачных попытках аутентификации
    """
    ip_address = models.GenericIPAddressField("IP адрес")
    attempts = models.IntegerField("Неудачных попыток", default=0)
    time_unblock = models.DateTimeField("Время разблокировки", blank=True)
    status = models.BooleanField("Статус блокировки", default=False)

    class Meta:
         verbose_name = 'Неудачные попытки входа'
         verbose_name_plural = 'Неудачные попытки входа'

    def __str__(self):
        return self.ip_address
