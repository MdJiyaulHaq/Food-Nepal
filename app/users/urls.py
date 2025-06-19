from django.urls import path
from users.views import (
    UserCreateView,
    UserDeleteView,
    UserLoginView,
    UserRetrieveView,
    UserUpdateView,
)

app_name = "users"

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="create-user"),
    path("token/", UserLoginView.as_view(), name="user-login"),
    path("me/", UserRetrieveView.as_view(), name="user-retrieve"),
    path("update/", UserUpdateView.as_view(), name="user-update"),
    path("delete/", UserDeleteView.as_view(), name="user-delete"),
]
