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
        fields = ("id", "profile", "designation")

class ContactCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        contact = Contact.objects.create(
            designation=data['designation'],
            profile= data['profile'],
        )
        contact.save()
        return contact

    class Meta:
        model = Contact
        fields = ("id", "profile", "designation")

class UpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        #pylint: disable=no-member
        model = Update
        read_only_fields = ("id","author","upvotes", "downvotes")
        fields=("id","title","description","author","date","upvotes", "downvotes")

class UpdateCreateSerializer(serializers.ModelSerializer):

    author=serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        #pylint: disable=no-member
        model = Update
        read_only_fields = ("id","author","upvotes", "downvotes")
        fields=("id","title","description","author","date","upvotes", "downvotes")


class SuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        #pylint: disable=no-member
        model = Suggestion
        read_only_fields = ("id","author","upvotes", "downvotes")
        fields=("id","title","description","author","date","upvotes", "downvotes")

class SuggestionCreateSerializer(serializers.ModelSerializer):

    author=serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        #pylint: disable=no-member
        model = Suggestion
        read_only_fields = ("id","author","upvotes", "downvotes")
        fields=("id","title","description","author","date","upvotes", "downvotes")
