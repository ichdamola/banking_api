# 3rd party imports
import jwt
from rest_framework import authentication, exceptions

# system imports
from django.conf import settings

from . import models


class CustomUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=["HS256"]
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed("Token is invalid")

        user_id = payload.get("id")
        if not user_id:
            raise exceptions.AuthenticationFailed(
                "Token does not contain user ID"
            )

        user = models.User.objects.filter(id=user_id).first()
        if not user:
            raise exceptions.AuthenticationFailed("User not found")

        return (user, None)
