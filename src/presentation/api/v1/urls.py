from rest_framework.routers import SimpleRouter

from presentation.controllers.conversation.conversation_views import ConversationModelViewSet

router = SimpleRouter()

# Conversation
router.register("conversation", ConversationModelViewSet, basename="conversation")

urlpatterns = router.urls
