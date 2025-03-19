from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import CharField, PasswordInput, MultipleChoiceField, EmailField
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from domain.base import CustomModelAdmin, CustomModelForm
from infrastructure.exceptions.exceptions import PasswordMissmatchException


User = get_user_model()

class UserCreationForm(CustomModelForm):
    email = EmailField(required=False)
    password1 = CharField(label="Password", widget=PasswordInput)
    password2 = CharField(label="Password confirmation", widget=PasswordInput)

    class Meta:
        model = User
        fields = [
            "email",
            "is_active",
            "is_verified",
            "is_staff",
            "is_hidden",
            "is_vip",
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise PasswordMissmatchException()
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(CustomModelForm):
    email = CharField(required=False)
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = [
            "email",
            "is_active",
            "is_verified",
            "is_staff",
            "is_hidden",
            "is_vip",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )


class CustomUserAdmin(UserAdmin, CustomModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "id",
        "email",
        "last_login",
        "date_joined",
        "last_used_ip",
        "is_staff",
        "is_active",
        "is_superuser",
        "is_hidden",
        "is_vip",
        "is_verified",
    )
    search_fields = ("id", "email")
    ordering = search_fields
    fieldsets = (
        ("Authentication", {"fields": ("email", "password")}),
        (
            "Permission",
            {"fields": ("is_staff", "is_active", "is_hidden", "is_verified", "is_vip")},
        ),
        ("Group Permissions", {"fields": ("groups", "user_permissions")}),
        (
            "Metadata",
            {"fields": ("last_login", "date_joined", "last_used_ip")},
        ),
    )
    add_fieldsets = (
        (
            "Authentication",
            {"fields": ("email", "password1", "password2")},
        ),
        (
            "Permission",
            {"fields": ("is_staff", "is_active", "is_hidden", "is_verified", "is_vip")},
        ),
        ("Group Permissions", {"fields": ("groups", "user_permissions")}),
        (
            "Metadata",
            {
                "fields": (
                    "date_joined",
                )
            },
        ),
    )

    def save_form(self, request, form, change):
        if not change:
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            additional = {
                "is_staff": form.cleaned_data["is_staff"],
                "is_active": form.cleaned_data["is_active"],
                "is_superuser": form.cleaned_data.get("is_superuser", False),
                "is_hidden": form.cleaned_data["is_hidden"],
                "is_verified": form.cleaned_data["is_verified"],
            }

            if additional["is_superuser"]:
                form.instance = self.model.super_users.create(
                    email=email,
                    password=password,
                    **additional,
                )

            else:
                form.instance = self.model.objects.create(
                    email=email,
                    password=password,
                    **additional,
                )
        return super().save_form(request, form, change)

admin.site.register(User, CustomUserAdmin)