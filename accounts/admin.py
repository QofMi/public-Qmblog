from django.contrib import admin
from .models import TemporaryBanIp


@admin.register(TemporaryBanIp)
class TemporaryBanIpAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'status', 'attempts', 'time_unblock')
    search_fields = ('ip_address',)
