from decimal import Decimal
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from core.models import Recipe, User


@pytest.fixture
def user():
    return baker.make(User, email="user@example.com")


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_create_recipe(client):
    url = reverse("recipe:recipe-list")
    data = {
        "title": "Test Recipe",
        "description": "This is a test recipe.",
        "time_minutes": 30,
        "price": "9.99",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Recipe.objects.count() == 1


@pytest.mark.django_db
def test_list_recipes(client, user):
    url = reverse("recipe:recipe-list")
    baker.make(Recipe, user=user, _quantity=5)

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db
def test_retrieve_recipe(client, user):
    recipe = baker.make(Recipe, user=user)
    url = reverse("recipe:recipe-detail", args=[recipe.pk])

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == recipe.pk
    assert response.data["title"] == recipe.title
    assert response.data["description"] == recipe.description
    assert response.data["time_minutes"] == recipe.time_minutes
    assert Decimal(response.data["price"]) == recipe.price


@pytest.mark.django_db
def test_update_recipe(client, user):
    recipe = baker.make(Recipe, user=user)
    url = reverse("recipe:recipe-detail", args=[recipe.pk])
    data = {
        "title": "Updated Recipe",
        "description": "This is an updated test recipe.",
        "time_minutes": 45,
        "price": "12.99",
    }

    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    recipe.refresh_from_db()
    assert recipe.title == data["title"]
    assert recipe.description == data["description"]
    assert recipe.time_minutes == data["time_minutes"]
    assert recipe.price == Decimal(data["price"])


@pytest.mark.django_db
def test_delete_recipe(client, user):
    recipe = baker.make(Recipe, user=user)
    url = reverse("recipe:recipe-detail", args=[recipe.pk])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Recipe.objects.filter(pk=recipe.pk).exists()
