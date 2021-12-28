from rest_framework import permissions
from .models import UserProfile

class AllowNoticeContact(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        if profile.can_post_notice:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        if profile.can_post_notice:
            return True
        return False
