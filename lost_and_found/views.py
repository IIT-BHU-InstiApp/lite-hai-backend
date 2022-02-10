from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import LostAndFound
from .serializers import (
    CreateLostAndFoundSerializer, CountLostAndFoundSerializer,
    LostAndFoundSerializer, LostAndFoundDetailSerializer)


class CreateLostAndFoundView(GenericAPIView):
    """
    post:
    Creates a new lost and found object and returns the
    Id, Name, Branch, Course, Year, Type, Description and Status of the object.
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


class CountLostAndFoundView(GenericAPIView):
    """
    get:
    Returns a dictionary consisting of number of closed, registered and pending lost and found objects.
    """
    permission_classes = (permissions.IsAuthenticated,)
    # pylint: disable=no-member
    queryset = LostAndFound.objects.all()
    serializer_class = CountLostAndFoundSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        count = serializer.get_count()
        return Response(count, status=status.HTTP_200_OK)


class LostAndFoundDetailView(GenericAPIView):
    """
    get:
    Returns the list of all lost and found objects created by the authenticated user
    having the given status value 'st'.
    """
    permission_classes = (permissions.IsAuthenticated,)
    # pylint: disable=no-member
    queryset = LostAndFound.objects.all()
    serializer_class = LostAndFoundDetailSerializer

    def get(self, request, st):
        serializer = self.get_serializer()
        detailed_complaints = serializer.get_details(status=st)
        detailed_complaints_dict = LostAndFoundSerializer(
            detailed_complaints, many=True)
        return Response(detailed_complaints_dict.data, status=status.HTTP_200_OK)
