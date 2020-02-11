from datetime import date
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .models import Workshop, Council, Club
from .serializers import (
    CouncilSerializer, CouncilDetailSerializer, ClubDetailSerializer,
    WorkshopSerializer, WorkshopCreateSerializer, WorkshopDetailSerializer)
from .permissions import AllowClubAdmin, AllowAdmin


class CouncilView(generics.ListAPIView):
    # pylint: disable=no-member
    queryset = Council.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CouncilSerializer


class CouncilDetailView(generics.RetrieveAPIView):
    # pylint: disable=no-member
    queryset = Council.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CouncilDetailSerializer


class ClubDetailView(generics.RetrieveAPIView):
    # pylint: disable=no-member
    queryset = Club.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = ClubDetailSerializer


class WorkshopView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopSerializer
    # pylint: disable=no-member
    queryset = Workshop.objects.filter(date__gte=date.today()).order_by('date', 'time')


class WorkshopPastView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopSerializer
    # pylint: disable=no-member
    queryset = Workshop.objects.filter(date__lt=date.today()).order_by('-date', '-time')


class WorkshopCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowAdmin,)
    serializer_class = WorkshopCreateSerializer

    def post(self, request):
        """
        Handles the POST request
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class WorkshopDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowClubAdmin,)
    serializer_class = WorkshopDetailSerializer
    # pylint: disable=no-member
    queryset = Workshop.objects.all()
