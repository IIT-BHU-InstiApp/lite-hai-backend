from datetime import date
from rest_framework import serializers
from .models import UserProfile, Club, Council, Workshop

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'email', 'phone_number', 'photo_url')


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'council', 'small_image_url', 'large_image_url')


class CouncilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Council
        fields = ('id', 'name', 'small_image_url', 'large_image_url')


class WorkshopSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)
    class Meta:
        model = Workshop
        fields = ('id', 'club', 'title', 'date', 'time',)


class WorkshopActivePastSerializer(serializers.Serializer):
    active_workshops = WorkshopSerializer()
    past_workshops = WorkshopSerializer()


class ClubDetailSerializer(serializers.ModelSerializer):
    council = CouncilSerializer()
    secy = serializers.SerializerMethodField()
    joint_secy = serializers.SerializerMethodField()
    active_workshops = serializers.SerializerMethodField()
    past_workshops = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    subscribed_users = serializers.SerializerMethodField()

    def get_secy(self, obj):
        """
        Get the the value of secy field
        """
        if obj.secy is None:
            return None
        serializer = UserProfileSerializer(obj.secy)
        return serializer.data

    def get_joint_secy(self, obj):
        """
        Get the the value of joint_secy field
        """
        serializer = UserProfileSerializer(obj.joint_secy, many=True)
        return serializer.data

    def get_active_workshops(self, obj):
        """
        Get the the value of active workshops field
        """
        # pylint: disable=no-member
        queryset = Workshop.objects.filter(
            club=obj, date__gte=date.today()).order_by('date', 'time')
        serializer = WorkshopSerializer(queryset, many=True)
        return serializer.data

    def get_past_workshops(self, obj):
        """
        Get the the value of past_workshops field
        """
        # pylint: disable=no-member
        queryset = Workshop.objects.filter(
            club=obj, date__lt=date.today()).order_by('-date', '-time')
        serializer = WorkshopSerializer(queryset, many=True)
        return serializer.data

    def get_is_subscribed(self, obj):
        """
        Get if the user has subscribed the club
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return None
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=user)
        return profile in obj.subscribed_users.all()

    def get_subscribed_users(self, obj):
        """
        Get the total number of subscribed users
        """
        return obj.subscribed_users.count()


    class Meta:
        model = Club
        fields = (
            'id', 'name', 'description', 'council', 'secy', 'joint_secy',
            'active_workshops', 'past_workshops', 'small_image_url', 'large_image_url',
            'is_subscribed', 'subscribed_users')


class ClubSubscriptionToggleSerializer(serializers.Serializer):
    def toggle_subscription(self):
        """
        Toggles the subscription of the user
        """
        user = self.context['request'].user
        if user.is_anonymous:
            raise serializers.ValidationError("User is not logged in")
        # pylint: disable=no-member
        profile = UserProfile.objects.get(
            user=user)
        club = self.context['club']

        if club in profile.subscriptions.all():
            club.subscribed_users.remove(profile)
        else:
            club.subscribed_users.add(profile)


class CouncilDetailSerializer(serializers.ModelSerializer):
    gensec = serializers.SerializerMethodField()
    joint_gensec = serializers.SerializerMethodField()
    clubs = serializers.SerializerMethodField()

    def get_gensec(self, obj):
        """
        Get the the value of secy field
        """
        if obj.gensec is None:
            return None
        serializer = UserProfileSerializer(obj.gensec)
        return serializer.data

    def get_joint_gensec(self, obj):
        """
        Get the the value of joint_secy field
        """
        serializer = UserProfileSerializer(obj.joint_gensec, many=True)
        return serializer.data

    def get_clubs(self, obj):
        """
        Get the the value of clubs field
        """
        serializer = ClubSerializer(obj.clubs, many=True)
        return serializer.data

    class Meta:
        model = Council
        fields = (
            'id', 'name', 'description', 'gensec', 'joint_gensec',
            'clubs', 'small_image_url', 'large_image_url')


class WorkshopCreateSerializer(serializers.ModelSerializer):
    def validate_club(self, club):
        """
        Validate the club field
        """
        request = self.context['request']
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        if club not in profile.get_club_privileges():
            raise serializers.ValidationError(
                "You are not authorized to create workshops for this club")
        return club

    def save(self, **kwargs):
        data = self.validated_data
        # pylint: disable=no-member
        workshop = Workshop.objects.create(
            title=data['title'], description=data['description'], club=data['club'],
            date=data['date'], time=data['time'], location=data['location'],
            audience=data['audience'], resources=data['resources'], image_url=data['image_url']
        )
        workshop.contacts.set(data['contacts'])
        # By default, add the creator of the workshop as the contact for the workshop
        workshop.contacts.add(UserProfile.objects.get(user=self.context['request'].user))

    class Meta:
        model = Workshop
        fields = (
            'id', 'title', 'description', 'club', 'date', 'time',
            'location', 'audience', 'resources', 'contacts', 'image_url')


class WorkshopDetailSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(allow_null=True, default=None)
    club = ClubSerializer(read_only=True, required=False)
    contacts = UserProfileSerializer(many=True, read_only=True)
    is_interested = serializers.SerializerMethodField()
    interested_users = serializers.SerializerMethodField()

    def get_is_interested(self, obj):
        """
        Get if the user is interested for the workshop
        """
        # pylint: disable=no-member
        user = self.context['request'].user
        if user.is_anonymous:
            return None
        profile = UserProfile.objects.get(user=user)
        return profile in obj.interested_users.all()

    def get_interested_users(self, obj):
        """
        Get the total number of interested users for the workshop
        """
        return obj.interested_users.count()

    class Meta:
        model = Workshop
        read_only_fields = ('club', 'contacts', 'is_interested', 'interested_users')
        fields = (
            'id', 'title', 'description', 'club', 'date', 'time',
            'location', 'audience', 'resources', 'contacts', 'image_url',
            'is_interested', 'interested_users')
