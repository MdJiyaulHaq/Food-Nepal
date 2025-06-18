app_name = "users"
from django.urls import path, include
from users.views import (
    UserCreateView,
    UserLoginView,
    UserRetrieveView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="create-user"),
    path("token/", UserLoginView.as_view(), name="user-login"),
    path("me/", UserRetrieveView.as_view(), name="user-retrieve"),
    path("update/", UserUpdateView.as_view(), name="user-update"),
    path("delete/", UserDeleteView.as_view(), name="user-delete"),
]
