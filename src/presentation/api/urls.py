"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from decouple import config

from presentation.controllers.sample import SampleViewSet
# from presentation.controllers.security import HoneypotLoginView

BASENAME = "api"
API_SCHEMA_PREFIX = "radigenius-api-schema"

urlpatterns = [
]

development_urls = [
    path("admin/", admin.site.urls),
    path("test/", SampleViewSet.as_view({"get": "retrieve"}, name="test")),
    path(
        f"{BASENAME}/{API_SCHEMA_PREFIX}/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        f"{BASENAME}/{API_SCHEMA_PREFIX}/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"{BASENAME}/{API_SCHEMA_PREFIX}/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]
production_urls = [
    # path("admin/", HoneypotLoginView.as_view(), name="honeypot-login"),
    path(f'{config("ADMIN_SECURE_LOGIN_ROUTE")}/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += development_urls
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += production_urls


handler400 = "presentation.controllers.base.custom_error_400"  # bad_request
handler403 = "presentation.controllers.base.custom_error_403"  # permission_denied
handler404 = "presentation.controllers.base.custom_error_404"  # page_not_found
handler500 = "presentation.controllers.base.custom_error_500"  # server_error
