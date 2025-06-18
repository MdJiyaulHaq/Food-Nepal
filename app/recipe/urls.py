from rest_framework.routers import DefaultRouter
from recipe import views
from django.urls import path, include

app_name = "recipe"

router = DefaultRouter()
router.register("", views.RecipeViewSet, basename="recipe")

urlpatterns = router.urls
