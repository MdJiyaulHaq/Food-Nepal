app_name = "users"
from django.urls import path, include
from users.views import UserCreateView

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="create-user"),
]
