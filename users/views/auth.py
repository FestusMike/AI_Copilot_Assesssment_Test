from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from django.core import exceptions as dj_exceptions
from rest_framework import viewsets, status, permissions as rest_permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from users.serializers import UserLoginSerializer, UserLogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions as rest_exceptions
from includes.helpers.auth_handler import UserAuthHandler
from includes.drf import APIResponseSerializer


@extend_schema_view(
    login=extend_schema(
        request=UserLoginSerializer,
        responses={200: OpenApiResponse(response=APIResponseSerializer)},
        summary="User Login",
        description="Authenticates a user with email and password and returns JWT access and refresh tokens.",
        tags=["Authentication"],
    ),
    logout=extend_schema(
        request=UserLogoutSerializer,
        responses={200: OpenApiResponse(response=APIResponseSerializer)},
        summary="User Logout",
        description="Logs out a user by blacklisting their refresh token.",
        tags=["Authentication"],
    ),
)
class UserAuthViewSet(viewsets.GenericViewSet):
    permission_classes = [rest_permissions.AllowAny]

    @action(
        detail=False, methods=["post"], url_path="user-login", url_name="user-login"
    )
    def login(self, request: Request) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        try:
            login_response = UserAuthHandler().login(email=email, password=password)
        except dj_exceptions.ValidationError as exc:
            raise rest_exceptions.ValidationError(f"{exc.message}", code=exc.code)
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "User logged in successfully",
                    "data": login_response,
                }
            ).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False, methods=["post"], url_path="user-logout", url_name="user-logout"
    )
    def logout(self, request: Request) -> Response:
        serializer = UserLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data.get("refresh")
        if not refresh_token:
            raise rest_exceptions.ValidationError(
                "Refresh token is required for logout."
            )
        try:
            UserAuthHandler().logout(RefreshToken(refresh_token))
        except dj_exceptions.ValidationError:
            raise rest_exceptions.ValidationError(
                "Logout Unsuccessful", code="logout_unsuccessful"
            )
        except Exception:
            raise rest_exceptions.ValidationError(
                "Logout Unsuccessful", code="logout_unsuccessful"
            )

        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "User logged out successfully",
                    "data": None,
                }
            ).data,
            status=status.HTTP_200_OK,
        )
