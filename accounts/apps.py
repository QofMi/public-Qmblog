from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'Глиномесы'

    def ready(self):
        import accounts.signals
