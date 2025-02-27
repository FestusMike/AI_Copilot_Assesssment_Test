from drf_spectacular.utils import extend_schema_view, extend_schema
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, parsers, permissions as rest_permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from users.serializers import (
    UserRegistrationSerializer,
)

from includes.drf import APIResponseSerializer


UserAccount = get_user_model()


@extend_schema_view(
    register=extend_schema(
        request=UserRegistrationSerializer,
        responses=APIResponseSerializer,
        summary="Register a new user",
        description="Registers a new user.",
        tags=["Accounts"],
    ),
)
class UserAccountViewSet(viewsets.GenericViewSet):
    permission_classes = [rest_permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    @action(
        detail=False,
        methods=["post"],
        url_path="user-registration",
        url_name="user-registration",
    )
    def register(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        skills = serializer.validated_data["skills"]

        serializer.save()

        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_201_CREATED,
                    "success": True,
                    "message": "Registration successful.",
                    "data": {
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "skills": skills,
                    },
                }
            ).data,
            status=status.HTTP_201_CREATED,
        )
