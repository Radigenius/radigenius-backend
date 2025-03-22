from django.contrib import admin

from domain.base import CustomModelAdmin, CustomGenericStackedInline, CustomModelForm
from domain.apps.system.models import Model

class ModelInline(CustomGenericStackedInline):
    model = Model
    extra = 0


class CustomModelAddChangeForm(CustomModelForm):
    class Meta:
        model = Model
        fields = [
            "name",
            "description",
        ]

@admin.register(Model)
class CustomModelAdmin(CustomModelAdmin):
    model = Model
    form = CustomModelAddChangeForm
    add_form = CustomModelAddChangeForm
    list_display = (
        "id",
        "name",
        "description",
        "created_date",
    )