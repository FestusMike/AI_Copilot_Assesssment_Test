from django.core import exceptions as dj_exceptions
import string


def validate_password(value: str) -> None:
    if len(value) < 8:
        raise dj_exceptions.ValidationError(
            "Password must be at least 8 characters long", code="password_too_short"
        )
    if not any(c in string.digits for c in value) or not any(
        c in string.ascii_letters for c in value
    ):
        raise dj_exceptions.ValidationError(
            "Password must contain at least one digit and one letter",
            code="password_too_weak",
        )
