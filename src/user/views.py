from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import BomUser
from .serializers import UserSerializer


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
        data = serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        access_obj = AccessToken(data.get("access"))
        user_id = access_obj["user_id"]
        user = get_object_or_404(BomUser, pk=user_id)
        user.last_login = datetime.now()
        user.save()
        serialized_user = UserSerializer(user)
        data["user"] = serialized_user.data
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

