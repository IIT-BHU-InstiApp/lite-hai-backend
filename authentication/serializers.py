from rest_framework import serializers
from .utils import *
from .models import *
from rest_framework.exceptions import ParseError


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    id_token = serializers.CharField(max_length=2400)

    def validate_access_token(self, access_token):
        return FirebaseAPI.verify_id_token(access_token)
    
    def validate(self, data):
        id_token = data.get('id_token', None)
        user = None
        if id_token:
            jwt = self.validate_access_token(id_token)
            uid = jwt['uid']
            profile = UserProfile.objects.filter(uid=uid)
            try:
                profile = UserProfile.objects.get(uid=uid)
            except UserProfile.DoesNotExist:
                user = User()
                user.username = jwt['uid']
                user.last_name = FirebaseAPI.get_name(jwt)
                user.email = FirebaseAPI.get_email(jwt)
                if Student.verify_email(user.email):
                    pass
                else:
                    raise serializers.ValidationError("Please login using @itbhu.ac.in or @iitbhu.ac.in student email id only")
                department = Student.get_department(user.email)
                year_of_joining = Student.get_year(user.email)
                user.save()
                profile, created = UserProfile.objects.get_or_create(
                    uid=uid, user=user, name=user.last_name, email=user.email,
                    department=department, year_of_joining=year_of_joining
                )
            user = profile.user
        else:
            raise ParseError('Provide id_token or username to continue.')

        if user:
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
        else:
            raise serializers.ValidationError('Unable to log in with provided credentials.')

        data['user'] = user
        return data


