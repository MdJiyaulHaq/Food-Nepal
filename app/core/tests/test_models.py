from django.contrib.auth import get_user_model
import pytest
from core.models import User, CustomUserManager
from typing import cast
from core.models import Tag, Ingredient
from model_bakery import baker


@pytest.mark.django_db
class TestUserModel:
    def test_create_user_with_email_and_password(self):
        email = "test@example.com"
        password = "testpassword"
        UserModel = get_user_model()
        assert isinstance(UserModel(), User)  # Helps Pylance infer type
        manager = cast(CustomUserManager, UserModel.objects)
        user = manager.create_user(email=email, password=password)
        assert user.email == email
        assert user.check_password(password)

    def test_create_superuser_with_email_and_password(self):
        email = "test@example.com"
        password = "testpassword"
        UserModel = get_user_model()
        assert isinstance(UserModel(), User)  # Helps Pylance infer type
        manager = cast(CustomUserManager, UserModel.objects)
        user = manager.create_superuser(email=email, password=password)
        assert user.email == email
        assert user.check_password(password)
        assert user.is_staff
        assert user.is_superuser

    def test_email_is_normalized_like_gmail_logic_only(self):
        manager = CustomUserManager()
        emails = [
            ("John.Doe@GMAIL.COM", "johndoe@gmail.com"),
            ("JOHNDOE+spam@GMAIL.com", "johndoe@gmail.com"),
            ("John+News.Letters@GMAIL.com", "john@gmail.com"),
            ("Mixed.Case+Anything@Gmail.Com", "mixedcase@gmail.com"),
            ("plainuser@gmail.com", "plainuser@gmail.com"),
        ]

        for raw_email, expected in emails:
            assert manager.normalize_an_email(raw_email) == expected


@pytest.mark.django_db
class TestTagModel:
    def test_create_tag(self):
        tag = baker.make(Tag, label="Vegan")
        assert str(tag) == "Vegan"
        assert tag.label == "Vegan"
        assert tag.user is not None


@pytest.mark.django_db
class TestIngredientModel:
    def test_create_ingredient(self):
        ingredient = baker.make(Ingredient, name="Salt")
        assert str(ingredient) == "Salt"
        assert ingredient.name == "Salt"
        assert ingredient.user is not None
