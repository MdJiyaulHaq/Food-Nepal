from rest_framework.routers import DefaultRouter
from recipe import views
from django.urls import path, include

app_name = "recipe"

router = DefaultRouter()
router.register("recipes", views.RecipeViewSet, basename="recipe")
router.register("ingredients", views.IngredientViewSet, basename="ingredient")


urlpatterns = [
    path("", include(router.urls)),
]
