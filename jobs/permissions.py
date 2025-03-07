from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an object to read, update, or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
