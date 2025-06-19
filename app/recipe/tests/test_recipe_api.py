from decimal import Decimal
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from core.models import Recipe, User
import tempfile
import os
from PIL import Image


@pytest.fixture
def user():
    return baker.make(User, email="user@example.com")


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
class TestRecipeAPI:
    def test_create_recipe(self, client):
        url = reverse("recipe:recipe-list")
        data = {
            "title": "Test Recipe",
            "description": "This is a test recipe.",
            "time_minutes": 30,
            "price": "9.99",
            "tags": [],
        }
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Recipe.objects.count() == 1

    def test_list_recipes(self, client, user):
        url = reverse("recipe:recipe-list")
        baker.make(Recipe, user=user, _quantity=5)

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    def test_retrieve_recipe(self, client, user):
        recipe = baker.make(Recipe, user=user)
        url = reverse("recipe:recipe-detail", args=[recipe.pk])

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == recipe.pk
        assert response.data["title"] == recipe.title
        assert response.data["description"] == recipe.description
        assert response.data["time_minutes"] == recipe.time_minutes
        assert Decimal(response.data["price"]) == recipe.price

    def test_update_recipe(self, client, user):
        recipe = baker.make(Recipe, user=user)
        url = reverse("recipe:recipe-detail", args=[recipe.pk])
        data = {
            "title": "Updated Recipe",
            "description": "This is an updated test recipe.",
            "time_minutes": 45,
            "price": "12.99",
            "tags": [],
        }

        response = client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        recipe.refresh_from_db()
        assert recipe.title == data["title"]
        assert recipe.description == data["description"]
        assert recipe.time_minutes == data["time_minutes"]
        assert recipe.price == Decimal(data["price"])

    def test_delete_recipe(self, client, user):
        recipe = baker.make(Recipe, user=user)
        url = reverse("recipe:recipe-detail", args=[recipe.pk])

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Recipe.objects.filter(pk=recipe.pk).exists()


@pytest.mark.django_db
class TestRecipeDetailAPI:
    def test_get_detail(self, client, user):
        recipe = baker.make(Recipe, user=user)
        url = reverse("recipe:recipe-detail", args=[recipe.pk])

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == recipe.pk
        assert response.data["title"] == recipe.title

    def test_update_detail(self, client, user):
        recipe = baker.make(Recipe, user=user)
        url = reverse("recipe:recipe-detail", args=[recipe.pk])
        data = {
            "title": "Updated Detail Title",
            "description": "Updated description.",
            "time_minutes": 60,
            "price": "15.00",
        }

        response = client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        recipe.refresh_from_db()
        assert recipe.title == data["title"]
        assert recipe.description == data["description"]
        assert recipe.time_minutes == data["time_minutes"]
        assert recipe.price == Decimal(data["price"])

    def test_delete_detail(self, client, user):
        recipe = baker.make(Recipe, user=user)
        url = reverse("recipe:recipe-detail", args=[recipe.pk])

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Recipe.objects.filter(pk=recipe.pk).exists()


@pytest.mark.django_db
class TestRecipeWithTag:
    def test_create_recipe_with_new_tags(self, client, user):
        url = reverse("recipe:recipe-list")
        payload = {
            "title": "Curry with Spices",
            "description": "Flavorful and rich.",
            "time_minutes": 40,
            "price": "15.50",
            "tags": [{"label": "Spicy"}, {"label": "Dinner"}],
        }

        response = client.post(url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        recipe = Recipe.objects.get(pk=response.data["id"])
        assert recipe.tags.count() == 2
        assert recipe.tags.filter(label="Spicy").exists()
        assert recipe.tags.filter(label="Dinner").exists()

    def test_retrieve_recipes_with_tags(self, client, user):
        tag1 = baker.make("core.Tag", user=user, label="Healthy")
        tag2 = baker.make("core.Tag", user=user, label="Quick")
        recipe = baker.make(Recipe, user=user)
        recipe.tags.set([tag1, tag2])

        url = reverse("recipe:recipe-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        labels = [tag["label"] for tag in response.data[0]["tags"]]
        assert "Healthy" in labels
        assert "Quick" in labels

    def test_update_recipe_add_existing_tags(self, client, user):
        recipe = baker.make(Recipe, user=user)
        tag = baker.make("core.Tag", user=user, label="Vegetarian")  # noqa
        url = reverse("recipe:recipe-detail", args=[recipe.pk])
        payload = {
            "tags": [{"label": "Vegetarian"}],
        }

        response = client.patch(url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        recipe.refresh_from_db()
        assert recipe.tags.count() == 1
        assert recipe.tags.filter(label="Vegetarian").exists()


# @pytest.mark.django_db
# class TestRecipeWithIngredient:
#     def test_create_recipe_with_ingredients(self, client, user):
#         url = reverse("recipe:recipe-list")
#         payload = {
#             "title": "Pasta Primavera",
#             "description": "Classic pasta with vegetables.",
#             "time_minutes": 25,
#             "price": "10.00",
#             "ingredients": [{"name": "Pasta"}, {"name": "Zucchini"}],
#             "tags": [],
#         }

#         response = client.post(url, payload, format="json")

#         assert response.status_code == status.HTTP_201_CREATED
#         recipe = Recipe.objects.get(pk=response.data["id"])
#         assert recipe.ingredients.count() == 2
#         assert recipe.ingredients.filter(name="Pasta").exists()
#         assert recipe.ingredients.filter(name="Zucchini").exists()

#     def test_create_recipe_with_existing_ingredients(self, client, user):
#         ingredient1 = baker.make("core.Ingredient", user=user, name="Garlic")
#         ingredient2 = baker.make("core.Ingredient", user=user, name="Olive Oil")
#         url = reverse("recipe:recipe-list")
#         payload = {
#             "title": "Garlic Pasta",
#             "description": "Simple and delicious.",
#             "time_minutes": 20,
#             "price": "8.00",
#             "ingredients": [{"name": "Garlic"}, {"name": "Olive Oil"}],
#             "tags": [],
#         }

#         response = client.post(url, payload, format="json")

#         assert response.status_code == status.HTTP_201_CREATED
#         recipe = Recipe.objects.get(pk=response.data["id"])
#         assert recipe.ingredients.count() == 2
#         assert recipe.ingredients.filter(name="Garlic").exists()
#         assert recipe.ingredients.filter(name="Olive Oil").exists()


@pytest.mark.django_db
class TestRecipeImageUpload:
    def test_upload_image_to_recipe(self, client, user):
        recipe = baker.make("core.Recipe", user=user)
        url = reverse("recipe:recipe-upload-image", args=[recipe.pk])

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as image_file:
            img = Image.new("RGB", (100, 100))
            img.save(image_file, format="JPEG")
            image_file.seek(0)

        with open(image_file.name, "rb") as img_file:
            response = client.post(url, {"image": img_file}, format="multipart")

        os.remove(image_file.name)

        assert response.status_code == status.HTTP_200_OK
        recipe.refresh_from_db()
        assert bool(recipe.image)

        # Delete image file from media storage
        if recipe.image and os.path.exists(recipe.image.path):
            os.remove(recipe.image.path)
