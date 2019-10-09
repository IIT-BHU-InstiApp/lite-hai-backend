from rest_framework import serializers
from .utils import *
from .models import *
from rest_framework.exceptions import ParseError


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500)


class RegisterSerializer(serializers.Serializer):
    id_token = serializers.CharField(max_length=2400)
    mobile_number = serializers.CharField(max_length=15)
    roll_number = serializers.CharField(max_length=8)

    def validate_id_token(self, access_token):
        return FirebaseAPI.verify_id_token(access_token)
    
    def validate_mobile_number(self, mobile_number):
        if len(mobile_number) != 10 or not 6 <= int(mobile_number[0]) <= 9:
            raise serializers.ValidationError("Invalid 10 digit mobile number")
        return mobile_number
    
    def validate(self, data):
        jwt = data['id_token']
        email = FirebaseAPI.get_email(jwt)
        if Student.verify_email(email):
            pass
        else:
            raise serializers.ValidationError("Please login using @itbhu.ac.in or @iitbhu.ac.in student email id only")
        if Student.verify_roll_number(data['roll_number'], email):
            return data
        else:
            raise serializers.ValidationError("Invalid Roll Number")

    def get_user(self, jwt):
        user = User()
        user.username = jwt['uid']
        user.first_name = FirebaseAPI.get_name(jwt)
        user.email = FirebaseAPI.get_email(jwt)
        return user
    
    def create(self, validated_data):
        data = validated_data
        jwt = data['id_token']
        uid = jwt['uid']
        user = self.get_user(jwt)
        try:
            user.validate_unique()
        except Exception as e:
            raise serializers.ValidationError("Already Registered. Please login.")
        mobile_number = data['mobile_number']
        roll_number = data['roll_number']
        department = Student.get_department(user.email)
        year_of_joining = Student.get_year(user.email)
        course = Student.get_course(roll_number)
        user.save()
        profile, created = UserProfile.objects.get_or_create(
            uid=uid, user=user, name=user.first_name, email=user.email, roll_number=roll_number,
            mobile_number=mobile_number, department=department, course=course, year_of_joining=year_of_joining
        )
        return user


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
            
            try:
                profile = UserProfile.objects.get(uid=uid)
            except UserProfile.DoesNotExist:
                raise serializers.ValidationError('No such account exists')
            
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


