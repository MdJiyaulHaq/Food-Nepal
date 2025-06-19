import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from core.models import Ingredient, User


@pytest.fixture
def user():
    return baker.make(User, email="user@example.com")


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
class TestIngredientAPI:
    def test_create_ingredient(self, client):
        url = reverse("recipe:ingredient-list")
        payload = {"name": "Tomato"}

        response = client.post(url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Ingredient.objects.filter(name="Tomato").exists()

    def test_list_ingredients(self, client, user):
        baker.make(Ingredient, user=user, name="Salt")
        baker.make(Ingredient, user=user, name="Pepper")

        url = reverse("recipe:ingredient-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        names = [item["name"] for item in response.data]
        assert "Salt" in names
        assert "Pepper" in names

    def test_update_ingredient(self, client, user):
        ingredient = baker.make(Ingredient, user=user, name="Cumin")
        url = reverse("recipe:ingredient-detail", args=[ingredient.pk])
        payload = {"name": "Ground Cumin"}

        response = client.patch(url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        ingredient.refresh_from_db()
        assert ingredient.name == "Ground Cumin"

    def test_delete_ingredient(self, client, user):
        ingredient = baker.make(Ingredient, user=user, name="Onion")
        url = reverse("recipe:ingredient-detail", args=[ingredient.pk])

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Ingredient.objects.filter(pk=ingredient.pk).exists()
