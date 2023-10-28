from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from datetime import datetime, timedelta


class CookieBaseJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        request.META[
            "HTTP_AUTHORIZATION"
        ] = f'Bearer {request.COOKIES.get("access_token")}'
        return super().get_header(request)

    def authenticate(self, request):
        # Allow unauthenticated requests for registration endpoint
        if request.path == "/api/register/":
            return None

        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")
        try:
            AccessToken(access_token)
        except:
            if refresh_token:
                try:
                    refresh = RefreshToken(refresh_token)
                    new_access_token = refresh.access_token
                    request.COOKIES["access_token"] = new_access_token
                except:
                    raise InvalidToken(
                        {
                            "detail": _("Given token not valid for any token type"),
                            "messages": "refresh token is not valid or has been expired ! please login again!",
                        }
                    )

        return super().authenticate(request)


class SetCookiesMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        res = self.get_response(request)
        if request.COOKIES.get("access_token"):
            res.set_cookie(
                key="access_token",
                value=request.COOKIES.get("access_token"),
                httponly=True,
                secure=True,
                samesite="Strict",
                expires=datetime.now() + timedelta(days=30)
            )
        if request.COOKIES.get("refresh_token"):
            res.set_cookie(
                key="refresh_token",
                value=request.COOKIES.get("refresh_token"),
                httponly=True,
                secure=True,
                samesite="Strict",
                expires=datetime.now() + timedelta(days=30)
            )

        return res
