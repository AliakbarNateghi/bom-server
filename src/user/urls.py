from django.urls import include, path
from rest_framework import routers

from .views import GroupsViewSet, Login, Logout, UserInfo, UserRegistrationView

router = routers.DefaultRouter()

router.register(r"user-info", UserInfo, basename="user-info")
router.register(r"groups", GroupsViewSet, basename="groups")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
]
