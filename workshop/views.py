from datetime import date
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from authentication.models import UserProfile
from .models import Workshop, Council, Club
from .serializers import (
    CouncilSerializer, CouncilDetailSerializer, ClubDetailSerializer,
    WorkshopSerializer, WorkshopCreateSerializer, WorkshopDetailSerializer,
    WorkshopActiveAndPastSerializer, ClubSubscriptionToggleSerializer,
    WorkshopSearchSerializer, WorkshopDateSearchSerializer, WorkshopContactsUpdateSerializer,
    WorkshopInterestedToggleSerializer,)
from .permissions import AllowAnyClubHead, AllowWorkshopHead, AllowWorkshopHeadAndContacts


class ClubDetailView(generics.RetrieveAPIView):
    """
    Get the Name, Description, Council, Secretaries, Workshops, Image URL\
    and Subscribed Users details of a Club.
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
    permission_classes = (permissions.IsAuthenticated, )
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
        Toggles the Club Subscription for current user.
        """
        serializer = self.get_serializer()
        serializer.toggle_subscription()
        return Response(status=status.HTTP_200_OK)


class CouncilView(generics.ListAPIView):
    """
    Get the Name and Image URL of all Councils.
    """
    # pylint: disable=no-member
    queryset = Council.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CouncilSerializer


class CouncilDetailView(generics.RetrieveAPIView):
    """
    Get the Name, Description, Secretaries, Clubs and Image URL of a Council.
    """
    # pylint: disable=no-member
    queryset = Council.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CouncilDetailSerializer


class WorkshopActiveAndPastView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopActiveAndPastSerializer

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    # pylint: disable=unused-argument
    def get(self, *args, **kwargs):
        """
        Get both Active and Past Workshops.
        """
        # pylint: disable=no-member
        active_workshops = Workshop.objects.filter(
            date__gte=date.today()).order_by('date', 'time')
        past_workshops = Workshop.objects.filter(
            date__lt=date.today()).order_by('-date', '-time')
        active_workshops_serializer = WorkshopSerializer(active_workshops, many=True)
        past_workshops_serializer = WorkshopSerializer(past_workshops, many=True)
        serializer = WorkshopActiveAndPastSerializer(data={
            "active_workshops": active_workshops_serializer.data,
            "past_workshops": past_workshops_serializer.data
        })
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkshopActiveView(generics.ListAPIView):
    """
    Get the Active Workshops.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopSerializer
    # pylint: disable=no-member
    queryset = Workshop.objects.filter(date__gte=date.today()).order_by('date', 'time')


class WorkshopPastView(generics.ListAPIView):
    """
    Get the Past Workshops.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopSerializer
    # pylint: disable=no-member
    queryset = Workshop.objects.filter(date__lt=date.today()).order_by('-date', '-time')


class WorkshopCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowAnyClubHead,)
    serializer_class = WorkshopCreateSerializer

    def post(self, request):
        """
        Create Workshops for a Club - only Club POR Holders are allowed to create a workshop.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class WorkshopDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Get the title, description, club, date, time, location, audience, resources, contacts\
    and image URL for a workshop.
    Also, get the number of interested users for the workshop\
    and whether the user is interested for the workshop.

    put:
    Update the title, description, date, time, location, audience and resources of a workshop.
    Only the Club POR Holders and Workshop Contacts can update this. (Full Update)

    patch:
    Update the title, description, date, time, location, audience and resources of a workshop.
    Only the Club POR Holders and Workshop Contacts can update this. (Partial Update)

    delete:
    Delete the workshop. Only the Club POR Holders and Workshop Contacts can perform this action.
    """
    permission_classes = (AllowWorkshopHeadAndContacts,)
    serializer_class = WorkshopDetailSerializer
    # pylint: disable=no-member
    queryset = Workshop.objects.all()


class WorkshopContactsUpdateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowWorkshopHead,)
    serializer_class = WorkshopContactsUpdateSerializer
    lookup_field = 'pk'
    # pylint: disable=no-member
    queryset = Workshop.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'workshop':self.get_object()
        }

    # pylint: disable=unused-argument
    def put(self, request, pk):
        """
        Update the contacts of a workshop. Only the Club POR Holders can perform this action.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class WorkshopInterestedToggleView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = WorkshopInterestedToggleSerializer
    lookup_field = 'pk'
    # pylint: disable=no-member
    queryset = Workshop.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'workshop':self.get_object()
        }

    # pylint: disable=unused-argument
    def get(self, *args, **kwargs):
        """
        Toggles whether the user is interested for the workshop or not.
        """
        serializer = self.get_serializer()
        serializer.toggle_interested()
        return Response(status=status.HTTP_200_OK)


class WorkshopInterestedView(generics.ListAPIView):
    """
    Show all the workshops in which the user is interested.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WorkshopSerializer

    def get_queryset(self):
        # pylint: disable=no-member
        return UserProfile.objects.get(user=self.request.user).interested_workshops.all()


class WorkshopSearchView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopSearchSerializer

    def post(self, request):
        """
        Search a workshop based on Title, Location or Audience.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workshops = serializer.save()
        active_workshops = workshops.filter(date__gte=date.today()).order_by('date', 'time')
        past_workshops = workshops.filter(date__lt=date.today()).order_by('-date', '-time')
        active_workshops_serializer = WorkshopSerializer(active_workshops, many=True)
        past_workshops_serializer = WorkshopSerializer(past_workshops, many=True)
        serializer = WorkshopActiveAndPastSerializer(data={
            "active_workshops": active_workshops_serializer.data,
            "past_workshops": past_workshops_serializer.data
        })
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkshopDateSearchView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopDateSearchSerializer

    def post(self, request):
        """
        Search a workshop between the Start Date and End Date.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workshops = serializer.save()
        serializer = WorkshopSerializer(workshops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
