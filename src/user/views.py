from datetime import datetime

import numpy as np
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from ..core.permissions import IsOwner
from .models import BomUser
from .serializers import UserInfoSerializer, UserSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = BomUser.objects.create_user(**serializer.validated_data)
            user.set_password(serializer.validated_data["password"])
            user.save()
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
        res.delete_cookie("access_token")
        res.delete_cookie("refresh_token")
        return res


class UserInfo(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = BomUser.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "username"  # Specify the field to use for slug lookup

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
