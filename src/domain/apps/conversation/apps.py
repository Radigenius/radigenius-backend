from django.apps import AppConfig


class ConversationConfig(AppConfig):
    label = "conversation"
    name = "domain.apps.conversation"
    verbose_name = "conversation"

    def ready(self):
        import presentation.admin.conversation
