from rest_framework import permissions
from .models import UserProfile


class AllowWorkshopHead(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        # pylint: disable=no-member
        club = obj.club
        if club in profile.get_club_privileges():
            return True
        return False


class AllowWorkshopHeadOrContact(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        # pylint: disable=no-member
        club = obj.club
        if (club in profile.get_club_privileges()
                or obj in profile.organized_workshops.all()):
            return True
        return False


class AllowAnyClubHead(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        if profile.get_club_privileges():
            return True
        return False


class AllowAnyClubHeadOrContact(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        if profile.get_club_privileges() or profile.get_workshop_privileges():
            return True
        return False

class AllowWorkshopHeadOrContactForResource(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        # pylint: disable=no-member
        club = obj.workshop.club
        if (club in profile.get_club_privileges()
                or obj.workshop in profile.organized_workshops.all()):
            return True
        return False
