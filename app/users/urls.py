app_name = "users"
from django.urls import path, include
from users.views import UserCreateView, UserLoginView

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="create-user"),
    path("token/", UserLoginView.as_view(), name="user-login"),
]
