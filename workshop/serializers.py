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


class WorkshopActiveAndPastSerializer(serializers.Serializer):
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
            title=data['title'], description=data.get('description', ''), club=data['club'],
            date=data['date'], time=data.get('time', None), location=data.get('location', ''),
            audience=data.get('audience', ''), resources=data.get('resources', ''),
            image_url=data.get('image_url', '')
        )
        workshop.contacts.set(data.get('contacts', []))
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


class WorkshopContactsUpdateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        # pylint: disable=no-member
        workshop = self.context['workshop']
        workshop.contacts.set(data['contacts'])

    class Meta:
        model = Workshop
        fields = ('contacts',)


class WorkshopInterestedToggleSerializer(serializers.Serializer):
    def toggle_interested(self):
        """
        Toggles whether user is interested for the workshop or not.
        """
        user = self.context['request'].user
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=user)
        workshop = self.context['workshop']

        if workshop in profile.interested_workshops.all():
            workshop.interested_users.remove(profile)
        else:
            workshop.interested_users.add(profile)


class WorkshopInterestedSerializer(serializers.ModelSerializer):
    interested = serializers.SerializerMethodField()

    def get_interested(self, obj):
        """
        Get all the workshops in which the user is interested.
        """
        workshops = obj.interested_workshops.all()
        return WorkshopSerializer(workshops, many=True).data

    class Meta:
        model = UserProfile
        read_only_fields = ('interested',)
        fields = ('interested',)



class WorkshopSearchSerializer(serializers.Serializer):
    search_by = serializers.ChoiceField(choices=['title', 'location', 'audience'], default='title')
    search_string = serializers.CharField(max_length=50)

    def validate_search_string(self, search_string):
        """
        Validate the search_string field, length must be greater than 3
        """
        if len(search_string) < 3:
            raise serializers.ValidationError("The length of search field must be atleast 3")
        return search_string

    def save(self, **kwargs):
        data = self.validated_data
        search_by = data['search_by']
        search_string = data['search_string']
        # pylint: disable=no-member
        if search_by == 'title':
            workshop = Workshop.objects.filter(title__icontains=search_string)
        elif search_by == 'location':
            workshop = Workshop.objects.filter(location__icontains=search_string)
        elif search_by == 'audience':
            workshop = Workshop.objects.filter(audience__icontains=search_string)
        return workshop


class WorkshopDateSearchSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, attrs):
        """
        Validate the data i.e. start_date must be less than or equal to end_date
        """
        start_date = attrs['start_date']
        end_date = attrs['end_date']
        if start_date > end_date:
            raise serializers.ValidationError("Start Date cannot be greater than End Date")
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        start_date = data['start_date']
        end_date = data['end_date']
        # pylint: disable=no-member
        return Workshop.objects.filter(date__gte=start_date, date__lte=end_date)
