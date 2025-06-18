from django.shortcuts import render
from users.serializers import UserLoginSerializer, UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response({"token": f"fake-token-for-{user.email}"})
