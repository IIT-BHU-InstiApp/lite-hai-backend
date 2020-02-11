from rest_framework import serializers
from .models import *
import requests

def get_github_profile_pic_url(username):
    r = requests.get('https://api.github.com/users/' + username)
    github_user_json = r.json()
    return github_user_json['avatar_url']

class TeamMemberSerializer(serializers.ModelSerializer):
    github_image_url = serializers.SerializerMethodField()

    def get_github_image_url(self, obj):
        if not obj.github_image_url:
            obj.github_image_url = get_github_profile_pic_url(obj.github_username)
            obj.save()

        return obj.github_image_url

    class Meta:
        model = TeamMember
        fields = ('name', 'github_username', 'github_image_url')
