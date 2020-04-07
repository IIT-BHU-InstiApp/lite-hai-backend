from datetime import date
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .models import Workshop, Council, Club
from .serializers import (
    CouncilSerializer, CouncilDetailSerializer, ClubDetailSerializer,
    WorkshopSerializer, WorkshopCreateSerializer, WorkshopDetailSerializer,
    ClubSubscriptionToggleSerializer)
from .permissions import AllowClubAdmin, AllowAdmin


class ClubDetailView(generics.RetrieveAPIView):
    """
    Get the Name, Description, Council, Secretaries, Workshops, Image URL\
    and Subscribed Users details of a Club
    """
    # pylint: disable=no-member
    queryset = Club.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = ClubDetailSerializer

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'club':self.get_object()
        }


class ClubSubscriptionToggleView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ClubSubscriptionToggleSerializer
    lookup_field = 'pk'
    # pylint: disable=no-member
    queryset = Club.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'club':self.get_object()
        }

    # pylint: disable=unused-argument
    def get(self, *args, **kwargs):
        """
        Handles the GET request
        """
        serializer = self.get_serializer()
        serializer.toggle_subscription()
        return Response(status=status.HTTP_200_OK)


class CouncilView(generics.ListAPIView):
    """
    Get the Name and Image URL of all Councils
    """
    # pylint: disable=no-member
    queryset = Council.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CouncilSerializer


class CouncilDetailView(generics.RetrieveAPIView):
    """
    Get the Name, Description, Secretaries, Clubs and Image URL of a Council
    """
    # pylint: disable=no-member
    queryset = Council.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CouncilDetailSerializer


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
