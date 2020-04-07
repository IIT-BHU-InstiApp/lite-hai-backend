from django.core.validators import RegexValidator
from rest_framework import serializers
from workshop.serializers import ClubSerializer
from .utils import Student, FirebaseAPI
from .models import UserProfile, User

phone_regex = RegexValidator(
    regex=r'^\+\d{9,15}$',
    message="Phone number must be entered in the format: '+919876543210'."
)


class ResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    id_token = serializers.CharField(max_length=2400)

    def access_token_validate(self, access_token):
        """
        Validate the firebase access token
        """
        try:
            return FirebaseAPI.verify_id_token(access_token)
        except:
            raise serializers.ValidationError("Invalid Firebase Token")

    # pylint: disable=arguments-differ
    def validate(self, data):
        id_token = data.get('id_token', None)
        current_user = None
        jwt = self.access_token_validate(id_token)
        uid = jwt['uid']
        # pylint: disable=no-member
        profile = UserProfile.objects.filter(uid=uid)

        if profile:
            current_user = profile[0].user
        else:
            email = jwt['email']
            if not Student.verify_email(email):
                raise serializers.ValidationError(
                    "Please login using @itbhu.ac.in student email id only")
            name = jwt['name']
            user = User()
            user.username = jwt['uid']
            user.email = email
            user.save()
            current_user = user
            department = Student.get_department(email)
            year_of_joining = Student.get_year(email)
            # pylint: disable=no-member
            profile = UserProfile.objects.create(
                uid=uid, user=user, name=name, email=email, department=department,
                year_of_joining=year_of_joining, photo_url=jwt['picture'])

        data['user'] = current_user
        return data


class ProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15, validators=[phone_regex,], allow_blank=True)
    subscriptions = serializers.SerializerMethodField()
    club_privileges = serializers.SerializerMethodField()

    def get_subscriptions(self, obj):
        """
        Get the user subscriptions for the clubs
        """
        clubs = obj.subscriptions.all()
        return ClubSerializer(clubs, many=True).data

    def get_club_privileges(self, obj):
        """
        Get the privileges of the user for creating workshops
        Clubs - Secretary / Joint Secretary,
        Councils - General Secretary / Joint General Secretary
        """
        clubs = obj.club_secy.all()
        clubs = clubs | obj.club_joint_secy.all()
        council_gensec = obj.council_gensec
        council_joint_gensec = obj.council_joint_gensec
        for council in council_gensec.all():
            clubs = clubs | council.clubs.all()
        for council in council_joint_gensec.all():
            clubs = clubs | council.clubs.all()

        return ClubSerializer(clubs, many=True).data

    def update(self, instance, validated_data):
        name = validated_data['name']
        phone_number = validated_data['phone_number']
        # pylint: disable=no-member
        profile = UserProfile.objects.get(pk=instance.pk)
        profile.name = name
        profile.phone_number = phone_number
        profile.photo_url = FirebaseAPI.get_photo_url(profile.uid) # update photo_url of user
        profile.save()
        return profile

    class Meta:
        model = UserProfile
        read_only_fields = (
            'email', 'department', 'year_of_joining', 'subscriptions', 'club_privileges',
            'photo_url')
        fields = (
            'name', 'email', 'phone_number', 'department', 'year_of_joining',
            'subscriptions', 'club_privileges', 'photo_url')
