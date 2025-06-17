import json
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Ensure this field has at least 8 characters.")
        return value

    def validate(self, attrs):
        if "name" not in attrs or not attrs["name"]:
            raise serializers.ValidationError("Name is required.")
        if "email" not in attrs or not attrs["email"]:
            raise serializers.ValidationError("Email is required.")
        if "password" not in attrs or not attrs["password"]:
            raise serializers.ValidationError("Password is required.")
        return attrs
