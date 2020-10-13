from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_serializer_method
from .models import UserProfile, Club, Council, Workshop, Tag, WorkshopResource

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'email', 'phone_number', 'photo_url')


class CouncilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Council
        fields = ('id', 'name', 'small_image_url', 'large_image_url')


class ClubSerializer(serializers.ModelSerializer):
    council = CouncilSerializer()

    class Meta:
        model = Club
        fields = ('id', 'name', 'council', 'small_image_url', 'large_image_url')


class TagSerializer(serializers.ModelSerializer):
    club = ClubSerializer()

    class Meta:
        model = Tag
        fields = ('id', 'tag_name', 'club')


class WorkshopSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Workshop
        fields = ('id', 'club', 'title', 'date', 'time', 'tags')


class WorkshopActiveAndPastSerializer(serializers.Serializer):
    active_workshops = WorkshopSerializer()
    past_workshops = WorkshopSerializer()


class ClubDetailSerializer(serializers.ModelSerializer):
    council = CouncilSerializer(read_only=True, required=False)
    secy = serializers.SerializerMethodField()
    joint_secy = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    subscribed_users = serializers.SerializerMethodField()
    is_por_holder = serializers.SerializerMethodField()

    # @swagger_serializer_method(serializer_or_field=UserProfileSerializer)
    def get_secy(self, obj):
        """
        Secretary of the Club
        """
        if obj.secy is None:
            return None
        serializer = UserProfileSerializer(obj.secy)
        return serializer.data

    @swagger_serializer_method(serializer_or_field=UserProfileSerializer(many=True))
    def get_joint_secy(self, obj):
        """
        Joint Secretary of the Club
        """
        serializer = UserProfileSerializer(obj.joint_secy, many=True)
        return serializer.data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_subscribed(self, obj):
        """
        true, if the user has subscribed the club, otherwise false
        null, in case of anonymous login
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return None
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=user)
        return profile in obj.subscribed_users.all()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_subscribed_users(self, obj):
        """
        Total number of users subscribed to the club
        """
        return obj.subscribed_users.count()

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_por_holder(self, obj):
        """
        true, if the user is the POR Holder of the Club or Club's Council, otherwise false
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=user)
        if obj in profile.get_club_privileges():
            return True
        return False


    class Meta:
        model = Club
        read_only_fields = ('name', 'council', 'small_image_url', 'large_image_url')
        fields = (
            'id', 'name', 'description', 'council', 'secy', 'joint_secy',
            'small_image_url', 'large_image_url', 'is_subscribed', 'subscribed_users',
            'is_por_holder', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url',
            'linkedin_url', 'youtube_url')


class ClubDetailWorkshopSerializer(serializers.ModelSerializer):
    active_workshops = serializers.SerializerMethodField()
    past_workshops = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=WorkshopSerializer(many=True))
    def get_active_workshops(self, obj):
        """
        Active Workshops of the Club
        """
        # pylint: disable=no-member
        queryset = Workshop.objects.filter(
            club=obj, date__gte=date.today()).order_by('date', 'time')
        serializer = WorkshopSerializer(queryset, many=True)
        return serializer.data

    @swagger_serializer_method(serializer_or_field=WorkshopSerializer(many=True))
    def get_past_workshops(self, obj):
        """
        Past Workshops of the Club
        """
        # pylint: disable=no-member
        queryset = Workshop.objects.filter(
            club=obj, date__lt=date.today()).order_by('-date', '-time')
        serializer = WorkshopSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Club
        fields = ('active_workshops', 'past_workshops')


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
    is_por_holder = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=UserProfileSerializer)
    def get_gensec(self, obj):
        """
        General Secretary of the Council
        """
        if obj.gensec is None:
            return None
        serializer = UserProfileSerializer(obj.gensec)
        return serializer.data

    @swagger_serializer_method(serializer_or_field=UserProfileSerializer(many=True))
    def get_joint_gensec(self, obj):
        """
        Joint General Secretary of the Council
        """
        serializer = UserProfileSerializer(obj.joint_gensec, many=True)
        return serializer.data

    @swagger_serializer_method(serializer_or_field=ClubSerializer(many=True))
    def get_clubs(self, obj):
        """
        Clubs present in the Council
        """
        serializer = ClubSerializer(obj.clubs, many=True)
        return serializer.data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_por_holder(self, obj):
        """
        true, if the user is the POR Holder of the Council, otherwise false
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=user)
        if obj in profile.get_council_privileges():
            return True
        return False

    class Meta:
        model = Council
        read_only_fields = ('name', 'small_image_url', 'large_image_url')
        fields = (
            'id', 'name', 'description', 'gensec', 'joint_gensec',
            'clubs', 'small_image_url', 'large_image_url', 'is_por_holder', 'website_url',
            'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url')


class TagCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        """
        Validate whether the user can create the tag for the club,
        and whether the tag already exists
        """
        tag_name = attrs['tag_name']
        club = attrs['club']
        request = self.context['request']
        profile = UserProfile.objects.get(user=request.user)
        if (club not in profile.get_club_privileges() and
                club not in profile.get_workshop_privileges().values_list('club', flat=True)):
            raise PermissionDenied("You are not allowed to create tag for this club")
        if Tag.objects.filter(tag_name=tag_name, club=club):
            raise serializers.ValidationError("The tag already exists for this club")
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        tag = Tag.objects.create(tag_name=data['tag_name'], club=data['club'])
        return tag

    class Meta:
        model = Tag
        fields = ('id', 'tag_name', 'club')


class TagSearchSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        tag_name = data['tag_name']
        club = data['club']
        tags = Tag.objects.filter(tag_name__icontains=tag_name, club=club)
        return tags

    class Meta:
        model = Tag
        fields = ('id', 'tag_name', 'club')


class WorkshopTagsUpdateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        # pylint: disable=no-member
        workshop = self.context['workshop']
        workshop.tags.set(data['tags'])

    class Meta:
        model = Workshop
        fields = ('tags',)


class WorkshopCreateSerializer(serializers.ModelSerializer):
    def validate_club(self, club):
        """
        Validate the club field
        """
        request = self.context['request']
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=request.user)
        if club not in profile.get_club_privileges():
            raise PermissionDenied(
                "You are not authorized to create workshops for this club")
        return club

    def validate(self, attrs):
        """
        Validates whether the tags belong to the club for which the workshop is created
        """
        club = attrs['club']
        tags = attrs.get('tags', [])
        for tag in tags:
            if tag.club != club:
                raise serializers.ValidationError(
                    f"The tag {tag.tag_name} does not belong to this club")
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        # pylint: disable=no-member
        workshop = Workshop.objects.create(
            title=data['title'], description=data.get('description', ''), club=data['club'],
            date=data['date'], time=data.get('time', None), location=data.get('location', ''),
            latitude=data.get('latitude', None), longitude=data.get('longitude', None),
            audience=data.get('audience', ''), image_url=data.get('image_url', '')
        )
        workshop.contacts.set(data.get('contacts', []))
        workshop.tags.set(data.get('tags', []))
        # By default, add the creator of the workshop as the contact for the workshop
        workshop.contacts.add(UserProfile.objects.get(user=self.context['request'].user))

    class Meta:
        model = Workshop
        fields = (
            'id', 'title', 'description', 'club', 'date', 'time', 'location', 'latitude',
            'longitude', 'audience', 'contacts', 'image_url', 'tags',
            'link')


class WorkshopResourceSerializer(serializers.ModelSerializer):
    # pylint: disable=unused-argument
    def add_resource(self, **kwargs):
        """
        Handles the creation of a resource
        """
        data = self.validated_data
        # pylint: disable=no-member
        return WorkshopResource.objects.create(
            name=data['name'], link=data['link'], resource_type=data['resource_type'],
            workshop=self.context['workshop'])

    class Meta:
        model = WorkshopResource
        fields = (
            'id', 'name', 'link', 'resource_type'
        )

class WorkshopDetailSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(allow_null=True, default=None)
    club = ClubSerializer(read_only=True, required=False)
    contacts = UserProfileSerializer(many=True, read_only=True)
    resources = serializers.SerializerMethodField()
    is_interested = serializers.SerializerMethodField()
    interested_users = serializers.SerializerMethodField()
    is_workshop_contact = serializers.SerializerMethodField()
    is_por_holder = serializers.SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_interested(self, obj):
        """
        true, if the user is interested for the workshop, otherwise false
        null, in case of anonymous login
        """
        # pylint: disable=no-member
        user = self.context['request'].user
        if not user.is_authenticated:
            return None
        profile = UserProfile.objects.get(user=user)
        return profile in obj.interested_users.all()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_interested_users(self, obj):
        """
        Total number of users interested for the workshop
        """
        return obj.interested_users.count()

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_workshop_contact(self, obj):
        """
        true, if the user making the request is a workshop contact, otherwise false
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=user)
        return profile in obj.contacts.all()

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_por_holder(self, obj):
        """
        true, if the user is a POR holder of the Club or Club's Council, otherwise false
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        # pylint: disable=no-member
        profile = UserProfile.objects.get(user=user)

        if profile == obj.club.secy:
            return True

        if profile in obj.club.joint_secy.all():
            return True

        if profile == obj.club.council.gensec:
            return True

        if profile in obj.club.council.joint_gensec.all():
            return True

        return False

    @swagger_serializer_method(serializer_or_field=WorkshopResourceSerializer(many=True))
    def get_resources(self, obj):
        """
        All the resources for the workshop
        """
        return WorkshopResourceSerializer(obj.resources, many=True).data

    class Meta:
        model = Workshop
        read_only_fields = ('club', 'contacts', 'is_interested', 'interested_users', 'resources',
                            'tags')
        fields = (
            'id', 'title', 'description', 'club', 'date', 'time', 'location',
            'latitude', 'longitude', 'audience', 'resources', 'contacts', 'image_url',
            'is_interested', 'interested_users', 'is_workshop_contact', 'is_por_holder', 'tags',
            'link')


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

class ClubTagsSerializer(serializers.ModelSerializer):
    club_tags = serializers.SerializerMethodField()

    def get_club_tags(self, club):
        """
        Tags of a particular club
        """
        tags = Tag.objects.filter(club=club)
        serializer = TagSerializer(tags, many=True)
        return serializer.data
    class Meta:
        model = Club
        fields = ('club_tags',)
