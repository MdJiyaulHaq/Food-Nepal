from django.contrib import admin
from core.models import Ingredient, Tag, User, Recipe
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


class RecipeTagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin class for Recipe model."""

    list_display = ("id", "title", "user")
    search_fields = ("title",)
    ordering = ("id",)
    list_filter = ("user",)
    raw_id_fields = ("user",)
    autocomplete_fields = ("user",)
    inlines = [RecipeTagInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "label", "user"]
    readonly_fields = ["id"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "user"]
    readonly_fields = ["id"]
