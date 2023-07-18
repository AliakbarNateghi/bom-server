from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken, TokenError


class AuthenticationMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = None
        for header in scope["headers"]:
            if header[0] == b"authorization":
                token = header[1].decode("utf-8").split()[1]
                break
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            User = get_user_model()
            user = await database_sync_to_async(User.objects.get)(id=user_id)
            scope["user"] = user
        except TokenError:
            scope["user"] = AnonymousUser()
            await self.close()
        return await super().__call__(scope, receive, send)
