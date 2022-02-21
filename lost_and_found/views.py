from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import LostAndFound
from .serializers import (
    CreateLostAndFoundSerializer,
    LostAndFoundSerializer,
    LostAndFoundListSerializer)


class CreateLostAndFoundView(GenericAPIView):
    """
    post:
    Creates a new lost and found object and returns the
    Id, Name, Branch, Course, Year, Type and Description of the object.
    """
    permission_classes = (permissions.IsAuthenticated,)
    # pylint: disable=no-member
    queryset = LostAndFound.objects.all()
    serializer_class = CreateLostAndFoundSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        complaint = serializer.save()
        complaint_dict = LostAndFoundSerializer(complaint)
        return Response(complaint_dict.data, status=status.HTTP_201_CREATED)


class LostAndFoundListView(GenericAPIView):
    """
    get:
    Returns the list of all lost and found objects created by the authenticated user
    """
    permission_classes = (permissions.IsAuthenticated,)
    # pylint: disable=no-member
    queryset = LostAndFound.objects.all()
    serializer_class = LostAndFoundListSerializer

    def get(self, request):
        serializer = self.get_serializer()
        list_lost_and_found = serializer.get_list()
        list_lost_and_found_dict = LostAndFoundSerializer(
            list_lost_and_found, many=True)
        return Response(list_lost_and_found_dict.data, status=status.HTTP_200_OK)
