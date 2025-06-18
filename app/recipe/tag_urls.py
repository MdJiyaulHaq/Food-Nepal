from rest_framework.routers import DefaultRouter
from recipe.views import TagViewSet
from django.urls import path, include

router = DefaultRouter()
router.register("", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
]
