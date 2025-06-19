from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
class TestAdminSite:
    def test_admin_site(self, admin_client):
        """Test that the admin site is accessible."""
        response = admin_client.get(reverse("admin:index"))
        assert response.status_code == status.HTTP_200_OK

    def test_create_user(self, admin_client):
        """Test that a new user can be created via the admin."""
        User = get_user_model()
        data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        }
        response = admin_client.post(reverse("admin:core_user_add"), data)

        assert response.status_code == status.HTTP_302_FOUND
        assert User.objects.filter(email="testuser@example.com").exists()

    def test_user_list(self, admin_client):
        """Test that the user list is accessible."""
        response = admin_client.get(reverse("admin:core_user_changelist"))
        assert response.status_code == status.HTTP_200_OK

    def test_edit_user_page(self, admin_client):
        """Test that the edit user page is accessible."""
        # user = baker.make(get_user_model())
        user: Any = baker.make(get_user_model())
        response = admin_client.get(reverse("admin:core_user_change", args=[user.id]))
        assert response.status_code == status.HTTP_200_OK

    def test_create_user_page(self, admin_client):
        """Test that the create user page is accessible."""
        response = admin_client.get(reverse("admin:core_user_add"))
        assert response.status_code == status.HTTP_200_OK
