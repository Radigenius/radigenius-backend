from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from presentation.controllers.identity import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('generate/', CustomTokenObtainPairView.as_view(), name='jwt-generate'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]
