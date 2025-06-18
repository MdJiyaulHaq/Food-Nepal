from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipe APIs."""

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return recipes for the authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        """Create a new recipe and assign it to the authenticated user."""
        serializer.save(user=self.request.user)
