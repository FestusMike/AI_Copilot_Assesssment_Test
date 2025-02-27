from typing import TypedDict
from django.contrib import auth as dj_auth
from django.core import exceptions as dj_exceptions
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


UserAccount = dj_auth.get_user_model()


class LoginResponseDict(TypedDict):
    access: str
    refresh: str


class UserAuthHandler:
    @classmethod
    def login(cls, email: str, password: str) -> dict:
        try:
            user = UserAccount.objects.get(email__iexact=email)
        except UserAccount.DoesNotExist:
            raise dj_exceptions.ValidationError("Invalid email", code="invalid_email")

        if not user.check_password(password):
            raise dj_exceptions.ValidationError(
                "Invalid password", code="invalid_password"
            )

        user.last_login = timezone.now()
        user.save()
        refresh_token = RefreshToken.for_user(user)

        return LoginResponseDict(
            access=str(refresh_token.access_token), refresh=str(refresh_token)
        )

    @classmethod
    def logout(cls, refresh_token: RefreshToken) -> None:
        try:
            refresh_token.blacklist()
        except Exception:
            raise dj_exceptions.ValidationError(
                "Logout Unsuccessful", code="logout_unsuccessful"
            )
        return None
