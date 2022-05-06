# pylint: disable=too-few-public-methods
# from datetime import date
from rest_framework import serializers
from authentication.models import UserProfile
from .models import NoticeBoard

class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBoard
        fields = ("id", "title", "date", "importance", "description")

class NoticeDetailSerializer(serializers.ModelSerializer):
    has_voted = serializers.SerializerMethodField()

    def get_has_voted(self, obj):
        """Check if already voted"""
        # pylint: disable=no-member
        user = UserProfile.objects.get(user=self.context['request'].user)
        # if user in obj.voters.all():
        if obj.voters.filter(id = user.id).exists():
            return True
        return False

    class Meta:
        model = NoticeBoard
        read_only_fields = ("id", "upvotes", "downvotes")
        fields = ("id", "title", "description", "date", "upvotes", "downvotes",
                "importance", "has_voted")


class NoticeCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        # pylint: disable=no-member
        noticeBoard = NoticeBoard.objects.create(
            title=data["title"],
            description=data.get("description", ""),
            date=data["date"],
            upvotes=0,
            downvotes=0,
        )
        return noticeBoard
    class Meta:
        model = NoticeBoard
        fields = ("title", "description", "date", "importance")
