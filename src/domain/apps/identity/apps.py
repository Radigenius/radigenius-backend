from django.apps import AppConfig


class IdentityConfig(AppConfig):
    label = "identity"
    name = "domain.apps.identity"
    verbose_name = "Identity"

    def ready(self):
        import infrastructure.signals.identity.signals
        import presentation.admin.identity
