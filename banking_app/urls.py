# 3rd party imports
from rest_framework import routers

# system imports
from django.urls import path
from .views import *


router = routers.SimpleRouter()
router.register(r"accounts", AccountViewSet, basename="accounts")


urlpatterns = [
    path("users/create-user", CreateUserAPIView.as_view(), name="create"),
    path("users/login-user", LoginUserAPIView.as_view(), name="login"),
    path("users/logout-user", LogoutUserAPIView.as_view(), name="logout"),
    path(
        "users/get-logged-in-user",
        GetUserAPIView.as_view(),
        name="get_logged_user",
    ),
    path(
        "users/delete-current-user",
        DeleteCurrentUserAPIView.as_view(),
        name="delete-current-user",
    ),
    path(
        "users/update-current-user",
        UpdateCurrentUserAPIView.as_view(),
        name="update-current-user",
    ),
    path(
        "users/all",
        UserListAPIView.as_view(),
        name="users",
    ),
    path(
        "api/accounts/<int:id>/transactions/",
        TransactionList.as_view(),
        name="transaction-list",
    ),
]
