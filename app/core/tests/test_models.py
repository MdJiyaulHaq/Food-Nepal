from django.contrib.auth import get_user_model
import pytest
from core.models import User, CustomUserManager
from typing import cast


@pytest.mark.django_db
def test_create_user_with_email_and_password():
    email = "test@example.com"
    password = "testpassword"
    UserModel = get_user_model()
    assert isinstance(UserModel(), User)  # Helps Pylance infer type
    manager = cast(CustomUserManager, UserModel.objects)
    user = manager.create_user(email=email, password=password)
    assert user.email == email
    assert user.check_password(password)

@pytest.mark.django_db
def test_create_superuser_with_email_and_password():
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

@pytest.mark.django_db
def test_email_is_normalized_like_gmail_logic_only():
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
