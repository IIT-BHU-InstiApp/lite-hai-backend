from rest_framework import generics
from rest_framework import permissions
# from rest_framework import status
# from rest_framework.response import Response
from .serializers import RoleSerializer
from .models import Role

class TeamView(generics.ListAPIView):
    """
    Returns the list of all the people who have contributed to the making of this application.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = RoleSerializer
    # pylint: disable=no-member
    queryset = Role.objects.all()
