from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django.db.models.query import QuerySet
from django.http import HttpRequest

from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.admin import TabularInline, StackedInline


class CustomModelAdmin(ModelAdmin):

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return self.model.objects.all_objects()


class CustomModelForm(ModelForm):
    pass


class CustomGenericStackedInline(GenericStackedInline):
    extra = 0


class CustomTabularInline(TabularInline):
    extra = 0


class CustomStackedInline(StackedInline):
    extra = 0
