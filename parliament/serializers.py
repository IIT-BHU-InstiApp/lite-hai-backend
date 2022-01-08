# from datetime import date
from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from .models import ParliamentContact, ParliamentUpdate

class ParliamentContactListSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self,obj):
        serializer = ProfileSerializer(obj.profile)
        return serializer.data

    class Meta:
        model = ParliamentContact
        fields = ("id", "profile", "designation")

class ParliamentContactDetailSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self,obj):
        serializer = ProfileSerializer(obj.profile)
        return serializer.data

    class Meta:
        model = ParliamentContact
        fields = ("id", "profile", "designation")


class ParliamentContactCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        contact = ParliamentContact.objects.create(
            profile=self.context["profile"],
            designation=data["designation"]
        )
        contact.save()
        return contact

    class Meta:
        model = ParliamentContact
        fields = ("id", "designation")

class ParliamentUpdateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParliamentUpdate
        fields = ("id", "title", "date", "importance")

class ParliamentUpdateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParliamentUpdate
        fields = ("id", "title", "description", "date", "importance")


class ParliamentUpdateCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        # pylint: disable=no-member
        noticeBoard = ParliamentUpdate.objects.create(
            title=data["title"],
            description=data.get("description", ""),
            date=data["date"],
        )
        return noticeBoard
    class Meta:
        model = ParliamentUpdate
        fields = ("title", "description", "date", "importance")
