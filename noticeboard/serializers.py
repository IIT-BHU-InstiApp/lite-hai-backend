from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import NoticeBoard
from authentication.models import UserProfile


class NoticeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBoard
        fields = "__all__"


class NoticeCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        request = self.context["request"]
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        print(profile.get_workshop_privileges())
        if profile.get_workshop_privileges():
            raise PermissionDenied("You are not authorized to create notices")
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        # pylint: disable=no-member
        notice = NoticeBoard.objects.create(
            title=data["title"],
            description=data.get("description", ""),
            date=data.get("date", None),
            notice_url=data.get("link", None),
        )
        if data["pin"] == "true":
            notice.pin = True
        elif data["pin"] == "false":
            notice.pin = False
        notice.save()
        # FirebaseAPI.send_entity_message(data, self.context['notices'])
        return notice

    class Meta:
        model = NoticeBoard
        fields = ("title", "description", "date", "notice_url")