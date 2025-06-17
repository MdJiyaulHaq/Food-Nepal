from django.contrib import admin
from core.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Base admin class with common configurations."""

    list_display = ("email", "name")
    search_fields = ("email", "name")
    ordering = ("id",)
    fieldsets = (
        (None, {"fields": ("id", "email", "name", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    readonly_fields = ("id", "last_login")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
