from rest_framework import serializers
from .utils import *
from .models import *
from rest_framework.exceptions import ParseError


class ResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    id_token = serializers.CharField(max_length=2400)

    def validate_access_token(self, access_token):
        try:
            return FirebaseAPI.verify_id_token(access_token)
        except:
            raise serializers.ValidationError("Invalid Firebase Token")
    
    def validate(self, data):
        id_token = data.get('id_token', None)
        current_user = None
        jwt = self.validate_access_token(id_token)
        uid = jwt['uid']
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
                raise serializers.ValidationError("Please login using @itbhu.ac.in or @iitbhu.ac.in student email id only")
            department = Student.get_department(email)
            year_of_joining = Student.get_year(email)
            profile = UserProfile.objects.create(uid=uid,user=user,name=name,email=email,department=department,year_of_joining=year_of_joining)

        data['user'] = current_user
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name','email','department','year_of_joining')