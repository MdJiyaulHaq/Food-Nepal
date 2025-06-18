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
class TestTagAPI:
    def test_create_tag(self, client):
        url = reverse("tags:tag-list")
        data = {"label": "Vegan"}
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["label"] == data["label"]

    def test_list_tags(self, client, user):
        baker.make("core.Tag", user=user, label="Spicy")
        baker.make("core.Tag", user=user, label="Sweet")

        url = reverse("tags:tag-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        labels = [tag["label"] for tag in response.data]
        assert "Spicy" in labels and "Sweet" in labels

    def test_retrieve_tag(self, client, user):
        tag = baker.make("core.Tag", user=user, label="Healthy")

        url = reverse("tags:tag-detail", args=[tag.pk])
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["label"] == tag.label

    def test_update_tag(self, client, user):
        tag = baker.make("core.Tag", user=user, label="Breakfast")
        url = reverse("tags:tag-detail", args=[tag.pk])
        data = {"label": "Brunch"}

        response = client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        tag.refresh_from_db()
        assert tag.label == data["label"]

    def test_delete_tag(self, client, user):
        tag = baker.make("core.Tag", user=user, label="Dinner")
        url = reverse("tags:tag-detail", args=[tag.pk])

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not tag.__class__.objects.filter(pk=tag.pk).exists()
