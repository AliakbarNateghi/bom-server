from django.urls import path

from .views import Login, UserRegistrationView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/", Login.as_view(), name="login"),
]
