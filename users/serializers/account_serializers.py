from rest_framework import serializers
from typing import Type
from django.contrib import auth as dj_auth
from django.contrib.auth import models as dj_auth_models
from includes.helpers import utils
import re

UserAccount = dj_auth.get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[utils.validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    skills = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = UserAccount
        fields = ["email", "first_name", "last_name", "password", "password2", "skills"]
        extra_kwargs = {"skills": {"required": False}}

    def validate_first_name(self, value):
        """
        Validates the first name. Ensures it contains only letters and hyphens,
        starts and ends with a letter, and is between 2 and 32 characters.
        """
        if not re.match(r"^[a-zA-Z]([a-zA-Z-]{0,30}[a-zA-Z])$", value):
            raise serializers.ValidationError("Invalid first name.", code=400)
        return value

    def validate_last_name(self, value):
        """
        Validates the last name. Ensures it contains only letters and hyphens,
        starts and ends with a letter, and is between 2 and 32 characters.
        """
        if not re.match(r"^[a-zA-Z]([a-zA-Z-]{0,30}[a-zA-Z])$", value):
            raise serializers.ValidationError("Invalid last name.", code=400)
        return value

    def validate(self, attrs: dict) -> dict:
        password = attrs.get("password")
        password2 = attrs.get("password2")

        if password != password2:
            raise serializers.ValidationError("Passwords do not match", code=400)
        return attrs

    def create(self, validated_data: dict) -> Type[dj_auth_models.AbstractUser]:
        email = validated_data.get("email")
        first_name = validated_data.get("first_name").strip().capitalize()
        last_name = validated_data.get("last_name").strip().capitalize()
        password = validated_data.get("password").strip()
        skills = ",".join(validated_data.get("skills")) or None

        if UserAccount.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email already exists", code=400)

        user = UserAccount.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            skills=skills,
        )
        return user
