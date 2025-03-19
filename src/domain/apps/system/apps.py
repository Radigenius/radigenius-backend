from django.apps import AppConfig


class SystemConfig(AppConfig):
    label = "system"
    name = "domain.apps.system"
    verbose_name = "system"

    def ready(self):
        import infrastructure.signals.system.signals
        import presentation.admin.system
