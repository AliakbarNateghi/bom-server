from django.urls import include, path
from rest_framework import routers

from .views import Component, FieldPermissionView

router = routers.DefaultRouter()

router.register(r"components", Component, "components")
router.register(r"field-permission", FieldPermissionView, "field-permission")

urlpatterns = [
    path("", include(router.urls)),
]
