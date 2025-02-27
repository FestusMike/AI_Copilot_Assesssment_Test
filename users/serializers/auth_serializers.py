from rest_framework import serializers as rest_serializers


class UserLoginSerializer(rest_serializers.Serializer):
    email = rest_serializers.EmailField(required=True)
    password = rest_serializers.CharField(required=True)


class UserLogoutSerializer(rest_serializers.Serializer):
    refresh = rest_serializers.CharField(required=True)
