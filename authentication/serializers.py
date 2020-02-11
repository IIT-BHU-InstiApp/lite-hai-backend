from rest_framework import serializers
from workshop.serializers import ClubSerializer
from .utils import Student
from .models import UserProfile, User


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
            name = jwt['name']
            user = User()
            user.username = jwt['uid']
            user.email = email
            user.save()
            current_user = user

            if not Student.verify_email(email):
                raise serializers.ValidationError(
                    "Please login using @itbhu.ac.in or @iitbhu.ac.in student email id only")
            department = Student.get_department(email)
            year_of_joining = Student.get_year(email)
            # pylint: disable=no-member
            profile = UserProfile.objects.create(
                uid=uid, user=user, name=name, email=email, department=department,
                year_of_joining=year_of_joining)

        data['user'] = current_user
        return data


class ProfileSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = UserProfile
        read_only_fields = (
            'email', 'department', 'year_of_joining', 'subscriptions', 'club_privileges')
        fields = (
            'name', 'email', 'phone_number', 'department', 'year_of_joining',
            'subscriptions', 'club_privileges', 'photo_url')
