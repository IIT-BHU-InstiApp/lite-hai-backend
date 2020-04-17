from rest_framework import serializers
from .models import TeamMember, Role

class TeamMemberSerializer(serializers.ModelSerializer):
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
