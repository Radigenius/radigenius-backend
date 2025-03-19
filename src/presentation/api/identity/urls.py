from django.urls import path, include
from rest_framework.routers import SimpleRouter

from presentation.controllers.identity import (
    IdentityModelViewSet,
)

router = SimpleRouter()
router.register("users", IdentityModelViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
