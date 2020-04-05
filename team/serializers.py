from rest_framework import serializers
import requests
from .models import TeamMember, Role

def get_github_profile_pic_url(username):
    """
    Get the profile picture url from the github handle
    """
    r = requests.get('https://api.github.com/users/' + username)
    github_user_json = r.json()
    return github_user_json['avatar_url']

class TeamMemberSerializer(serializers.ModelSerializer):
    github_image_url = serializers.SerializerMethodField()

    def get_github_image_url(self, obj):
        """
        Get the value of github_image_url
        """
        if not obj.github_image_url:
            obj.github_image_url = get_github_profile_pic_url(obj.github_username)
            obj.save()

        return obj.github_image_url

    class Meta:
        model = TeamMember
        fields = ('name', 'github_username', 'github_image_url')


class RoleSerializer(serializers.ModelSerializer):
    team_members = serializers.SerializerMethodField()

    def get_team_members(self, obj):
        """
        Get the team members for a particular role
        """
        serializer = TeamMemberSerializer(obj.team_members, many=True)
        return serializer.data

    class Meta:
        model = Role
        fields = ('role', 'team_members')