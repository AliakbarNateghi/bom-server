from django.urls import include, path
from rest_framework import routers

from .views import Component

router = routers.DefaultRouter()

router.register(r"components", Component, "components")

urlpatterns = [
    path("", include(router.urls)),
]
