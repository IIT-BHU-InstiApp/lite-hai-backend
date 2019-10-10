from rest_framework import permissions
from .models import *


class AllowClubAdmin(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        profile = UserProfile.objects.filter(user=request.user)
        if profile and profile[0].is_admin:
            queryset = Workshop.objects.get(pk=obj.pk)
            club = queryset.club
            if club in profile[0].club_secy.all() or club in profile[0].club_joint_secy.all() or club in profile[0].workshop_contact.all():
                return True
            else:
                return False
        else:
            return False


class AllowAdmin(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_permission(self, request, view):
        profile = UserProfile.objects.filter(user=request.user)
        if profile and profile[0].is_admin:
            return True
        else:
            return False