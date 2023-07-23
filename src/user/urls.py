from django.urls import path, include
from rest_framework import routers

from .views import Login, UserRegistrationView, UserInfo


router = routers.DefaultRouter()

router.register(r'user-info', UserInfo, basename='user-info')
urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/", Login.as_view(), name="login"),
]