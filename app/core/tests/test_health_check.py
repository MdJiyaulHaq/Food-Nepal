from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class TestHealthCheckAPI(APITestCase):

    def test_health_check_returns_200(self):
        """Test that the health check endpoint returns HTTP 200"""
        url = reverse("health-check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_check_response_content(self):
        """Test the health check response content"""
        url = reverse("health-check")
        response = self.client.get(url)
        data = response.json()
        self.assertIn("status", data)
        self.assertEqual(data["status"], "ok")
