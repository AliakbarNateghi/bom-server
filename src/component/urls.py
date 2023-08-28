from django.urls import include, path
from rest_framework import routers

from .views import Component, FieldPermissionView, MassPermissionViewSet

router = routers.DefaultRouter()

router.register(r"components/(?P<table>[^/.]+)", Component, "components")
router.register(r"field-permission/(?P<table>[^/.]+)", FieldPermissionView, "field-permission")
router.register(r"mass-permission/(?P<table>[^/.]+)", MassPermissionViewSet, "mass-permission")

urlpatterns = [
    path("", include(router.urls)),
]
