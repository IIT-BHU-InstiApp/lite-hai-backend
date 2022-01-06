from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Complaint
from .serializers import (
    CreateGrievanceSerializer, CountGrievanceSerializer,
    GrievanceSerializer, GrievanceDetailSerializer)


class CreateGrievanceView(GenericAPIView):
    """
    post:
    Creates a new grievance object and returns the
    Id, Name, Branch, Course, Year, Type, Description, Drive Link and Status of the object.
    """
    permission_classes = (permissions.IsAuthenticated,)
    # pylint: disable=no-member
    queryset = Complaint.objects.all()
    serializer_class = CreateGrievanceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        complaint = serializer.save()
        complaint_dict = GrievanceSerializer(complaint)
        return Response(complaint_dict.data, status=status.HTTP_201_CREATED)


class CountGrievanceView(GenericAPIView):
    """
    get:
    Returns a dictionary consisting of number of closed, registered and pending grievances.
    """
    permission_classes = (permissions.IsAuthenticated,)
    # pylint: disable=no-member
    queryset = Complaint.objects.all()
    serializer_class = CountGrievanceSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        count = serializer.get_count()
        return Response(count, status=status.HTTP_200_OK)


class GrievanceDetailView(GenericAPIView):
    """
    get:
    Returns the list of all grievances created by the authenticated user
    having the given status value 'st'.
    """
    permission_classes = (permissions.IsAuthenticated,)
    # pylint: disable=no-member
    queryset = Complaint.objects.all()
    serializer_class = GrievanceDetailSerializer

    def get(self, request, st):
        serializer = self.get_serializer()
        detailed_complaints = serializer.get_details(status=st)
        detailed_complaints_dict = GrievanceSerializer(detailed_complaints, many=True)
        return Response(detailed_complaints_dict.data, status=status.HTTP_200_OK)
