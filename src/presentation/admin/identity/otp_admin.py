from django.contrib import admin
from domain.apps.identity.models import OTP
from domain.base import CustomModelAdmin

@admin.register(OTP)
class CustomOTPAdmin(CustomModelAdmin):
    model = OTP
    list_display = ("id", "code", "email", "active", "until", "created_date")
    search_fields = list_display
    list_filter = ("email",)

    @admin.display(empty_value=False)
    def active(self, obj):
        return obj.is_active

    active.boolean = True  # Display as a boolean (checkbox)