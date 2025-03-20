from rest_framework.routers import SimpleRouter

from presentation.controllers.conversation.conversation_views import ConversationGenericViewSet
from presentation.controllers.system.attachment_views import AttachmentGenericViewSet

router = SimpleRouter()

# Conversation
router.register("conversations", ConversationGenericViewSet, basename="conversations")

# System
router.register("system/attachments", AttachmentGenericViewSet, basename="attachments")

urlpatterns = router.urls
