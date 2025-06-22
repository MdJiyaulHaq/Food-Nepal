from django.shortcuts import render  # noqa

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok"})
