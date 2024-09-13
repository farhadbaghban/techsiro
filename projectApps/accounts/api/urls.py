from django.urls import path
from projectApps.accounts.api.views import (
    UserListApiView,
    UserRegisterApiView,
    UserLoginView,
    UserDeleteApiView,
)


app_name = "AccountUserApi"


urlpatterns = [
    path("register/", UserRegisterApiView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("list/", UserListApiView.as_view(), name="user-list"),
    path("delete/", UserDeleteApiView.as_view(), name="user-delete"),
]
