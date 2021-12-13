from rest_framework import permissions
from .models import UserProfile

class AllowNoticeContact(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        if profile.get_notice_privileges():
            return True
        return False
