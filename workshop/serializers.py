from rest_framework import serializers
from .models import *
from datetime import date


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'name',)


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name',)


class CouncilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Council
        fields = ('id', 'name',)


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ('id', 'title', 'date', 'time',)


class ClubDetailSerializer(serializers.ModelSerializer):
    council = CouncilSerializer()
    secy = serializers.SerializerMethodField()
    joint_secy = serializers.SerializerMethodField()
    workshops = serializers.SerializerMethodField()
    past_workshops = serializers.SerializerMethodField()

    def get_secy(self, obj):
        serializer = UserProfileSerializer(obj.secy)
        return serializer.data
    
    def get_joint_secy(self, obj):
        serializer = UserProfileSerializer(obj.joint_secy, many=True)
        return serializer.data
    
    def get_workshops(self, obj):
        queryset = Workshop.objects.filter(club=obj, date__gte=date.today()).order_by('date', 'time')
        serializer = WorkshopSerializer(queryset, many=True)
        return serializer.data
    
    def get_past_workshops(self, obj):
        queryset = Workshop.objects.filter(club=obj, date__lt=date.today()).order_by('-date', '-time')
        serializer = WorkshopSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Council
        fields = ('id', 'name', 'description', 'council', 'secy', 'joint_secy', 'workshops', 'past_workshops',)


class CouncilDetailSerializer(serializers.ModelSerializer):
    secy = serializers.SerializerMethodField()
    joint_secy = serializers.SerializerMethodField()
    clubs = serializers.SerializerMethodField()

    def get_secy(self, obj):
        serializer = UserProfileSerializer(obj.secy)
        return serializer.data
    
    def get_joint_secy(self, obj):
        serializer = UserProfileSerializer(obj.joint_secy, many=True)
        return serializer.data
    
    def get_clubs(self, obj):
        serializer = ClubSerializer(obj.clubs, many=True)
        return serializer.data

    class Meta:
        model = Council
        fields = ('id', 'name', 'description', 'secy', 'joint_secy', 'clubs',)


class WorkshopCreateSerializer(serializers.ModelSerializer):
    def validate_club(self, club):
        request = self.context['request']
        profile = UserProfile.objects.get(user=request.user)
        if club not in profile.club_secy.all() and club not in profile.club_joint_secy.all():
            raise serializers.ValidationError("You are not authorized to create workshops for this club")
        return club

    def validate_contacts(self, contacts):
        request = self.context['request']
        profile = UserProfile.objects.filter(user=request.user)
        if not profile:
            raise serializers.ValidationError("User does not exist")
        return contacts

    class Meta:
        model = Workshop
        fields = ('id', 'title', 'description', 'club', 'date', 'time', 'location', 'audience', 'resources', 'contacts',)


class WorkshopDetailSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)
    contacts = UserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Workshop
        fields = ('id', 'title', 'description', 'club', 'date', 'time', 'location', 'audience', 'resources', 'contacts',)