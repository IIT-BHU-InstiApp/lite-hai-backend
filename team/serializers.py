from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method
from .models import TeamMember, Role

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ('name', 'github_username', 'github_image_url')


class RoleSerializer(serializers.ModelSerializer):
    team_members = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=TeamMemberSerializer(many=True))
    def get_team_members(self, obj):
        """
        Team members for a particular role
        """
        serializer = TeamMemberSerializer(obj.team_members, many=True)
        return serializer.data

    class Meta:
        model = Role
        fields = ('role', 'team_members')
