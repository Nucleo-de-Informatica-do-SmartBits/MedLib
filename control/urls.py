from django.urls import path
from .views import * #noqa


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
]
