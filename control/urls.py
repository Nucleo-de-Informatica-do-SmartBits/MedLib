from django.urls import path
from .views import (
    signin,
    signup,
    logout
)

urlpatterns = [
    path(
        route="signup/",
        view=signup,
        name="signup"
    ),
    path(
        route="signin/",
        view=signin,
        name="signin"
    ),
    path(
        route="logout/",
        view=logout,
        name="logout"
    ),
]
