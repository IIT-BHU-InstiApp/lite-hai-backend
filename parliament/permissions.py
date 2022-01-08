from rest_framework import permissions
from .models import UserProfile

class AllowParliamentHead(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        if profile.can_add_parliament_details:
            return True
        return False
