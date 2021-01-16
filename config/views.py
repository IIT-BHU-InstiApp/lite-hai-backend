from rest_framework import generics
from rest_framework import permissions
from .serializers import ConfigVarSerializer
from .models import ConfigVar

class ConfigView(generics.ListAPIView):
    """
    Returns the list of all the config vars.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = ConfigVarSerializer
    # pylint: disable=no-member
    queryset = ConfigVar.objects.all()
