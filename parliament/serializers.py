# from datetime import date
from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from authentication.models import UserProfile
from .models import Contact, Update, Suggestion

class ContactsSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self,obj):
        serializer = ProfileSerializer(obj.profile)
        return serializer.data

    class Meta:
        model = Contact
        fields = ("id", "profile", "designation", "email", "phone")

class ContactCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        # Can't create anothor contact if you already have one.
        if Contact.objects.filter(profile=data["profile"]).exists():
            raise serializers.ValidationError("Contact already exists")
        contact = Contact.objects.create(
            designation=data['designation'],
            profile= data['profile'],
        )
        contact.save()
        return contact

    class Meta:
        model = Contact
        fields = ("id", "profile", "designation", "email", "phone")

class UpdateListSerializer(serializers.ModelSerializer):
    class Meta:
        #pylint: disable=no-member
        model = Update
        fields=("id","title","date", "committee")

class UpdateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        read_only_fields = ("id","author")
        fields=("id","title","description","author","date","committee")

class UpdateCreateSerializer(serializers.ModelSerializer):

    author=serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        #pylint: disable=no-member
        model = Update
        read_only_fields = ("id","author")
        fields=("id","title","description","author","date","committee")

class SuggestionListSerializer(serializers.ModelSerializer):
    class Meta:
        #pylint: disable=no-member
        model = Suggestion
        fields=("id","title","date")

class SuggestionDetailSerializer(serializers.ModelSerializer):
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
        model = Suggestion
        read_only_fields = ("id","author","upvotes", "downvotes")
        fields=("id","title","description","author","date","upvotes","downvotes","has_voted")


class SuggestionCreateSerializer(serializers.ModelSerializer):

    author=serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        #pylint: disable=no-member
        model = Suggestion
        read_only_fields = ("id","author","upvotes", "downvotes")
        fields=("id","title","description","author","date","upvotes", "downvotes")
