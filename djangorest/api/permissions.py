from rest_framework.permissions import BasePermission
from .models import Recommendation, Profile

class IsOwner(BasePermission):
    """Custom permission class to allow only recommendation owners to edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the recommendation owner."""
        if isinstance(obj, Recommendation):
            print(obj.owner)
            print(type(obj.owner))
            print(request.user)
            print(type(request.user))

            print(obj.owner == request.user)
            return obj.owner == request.user
        return obj.owner == request.user



class IsIdentifiedUser(BasePermission):
    """Custom permission class to allow only recommendation owners to edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the recommendation owner."""
        if isinstance(obj, Profile):
            print(obj.user)
            print(type(obj.user))
            print(request.user)
            print(type(request.user))

            print(obj.user == request.user)
            return obj.user == request.user
        return obj.user == request.user
