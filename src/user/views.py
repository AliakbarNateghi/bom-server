from datetime import datetime

import numpy as np
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from ..core.permissions import IsGod, IsOwner
from .models import BomUser, HiddenColumns
from .serializers import (
    GroupSerializer,
    HiddenColumnsSerializer,
    PasswordChangeSerializer,
    UserInfoSerializer,
    UserSerializer,
    UsersInfoReadOnlySerializer,
    UsersInfoWriteOnlySerializer,
)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = BomUser.objects.create_user(**serializer.validated_data)
            user.set_password(serializer.validated_data["password"])
            user.save()
            HiddenColumns.objects.create(user=user, hidden_cols={})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        access_obj = AccessToken(data.get("access"))
        user_id = access_obj["user_id"]
        user = get_object_or_404(BomUser, pk=user_id)
        user.last_login = datetime.now()
        user.save()
        serialized_user = UserSerializer(user)
        res = Response({"user": serialized_user.data}, status=status.HTTP_200_OK)
        res.set_cookie(
            key="access_token",
            value=data.get("access"),
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        res.set_cookie(
            key="refresh_token",
            value=data.get("refresh"),
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        return res


class Logout(APIView):
    def post(self, request, *args, **kwargs):
        res = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        # res.set_cookie('access_token', '', expires='Thu, 01 Jan 1970 00:00:00 GMT')
        # res.set_cookie('refresh_token', '', expires='Thu, 01 Jan 1970 00:00:00 GMT')

        res.delete_cookie("access_token")
        res.delete_cookie("refresh_token")
        return res


class UsersInfo(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = BomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "username"

    def get_serializer_class(self):
        method = self.request.method
        if method == "PUT" or method == "POST":
            return UsersInfoWriteOnlySerializer
        else:
            return UsersInfoReadOnlySerializer


class UserInfo(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = BomUser.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "username"

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save(username=self.request.user.username)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def change_password(self, request, username=None):
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            # Check if the old password matches the user's current password
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"error": "Invalid old pass"}, status=400)

            # Check if the new password and confirmation match
            if (
                serializer.validated_data["new_password"]
                != serializer.validated_data["confirm_password"]
            ):
                return Response({"error": "not match"}, status=400)

            # Set the new password and save the user
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response({"message": "success"}, status=200)

        return Response(serializer.errors, {"error": "wrong"}, status=400)


class GroupsViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsGod, IsAdminUser]


class HiddenColumnsViewSet(ModelViewSet):
    queryset = HiddenColumns.objects.all()
    serializer_class = HiddenColumnsSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            instance = self.queryset.get(user=self.request.user)
            instance.delete()
        except HiddenColumns.DoesNotExist:
            pass
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
