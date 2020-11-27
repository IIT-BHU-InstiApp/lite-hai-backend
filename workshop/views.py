from datetime import date
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from authentication.models import UserProfile
from .models import Workshop, Council, Club, WorkshopResource, Entity
from .serializers import (
    ClubTagDeleteSerializer, CouncilSerializer, CouncilDetailSerializer, ClubDetailSerializer, ClubDetailWorkshopSerializer, EntityTagDeleteSerializer,
    EntityTagSearchSerializer, EntityTagsSerializer, EntityDetailWorkshopSerializer,
    EntityWorkshopCreateSerializer, WorkshopSerializer,
    ClubWorkshopCreateSerializer, WorkshopDetailSerializer, ClubTagsSerializer,
    WorkshopActiveAndPastSerializer, ClubSubscriptionToggleSerializer,
    WorkshopSearchSerializer, WorkshopDateSearchSerializer, WorkshopContactsUpdateSerializer,
    WorkshopInterestedToggleSerializer, ClubTagCreateSerializer, ClubTagSearchSerializer,
    WorkshopTagsUpdateSerializer, WorkshopResourceSerializer,
    EntityDetailSerializer, EntitySubscriptionToggleSerializer,
    EntityTagCreateSerializer, EntitySerializer)
from .permissions import (
    AllowAnyClubHead, AllowAnyEntityHead, AllowAnyEntityHeadOrContact, AllowWorkshopHead,
    AllowAnyClubHeadOrContact, AllowWorkshopHeadOrContactForResource, AllowParticularCouncilHead,
    AllowParticularClubHead, AllowParticularEntityHead, AllowWorkshopHeadOrContact,)


class ClubDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
    Get the Name, Description, Council, Secretaries, Image URL\
    and Subscribed Users details of a Club.

    put:
    Update the description of a Club (Full Update).

    patch:
    Update the description of a Club (Partial Update).
    """
    # pylint: disable=no-member
    queryset = Club.objects.all()
    permission_classes = (AllowParticularClubHead,)
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
            'club': self.get_object()
        }


class EntityDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
    Get the Name, Description, Secretaries, Image URL\
    and Subscribed Users details of an Entity.

    put:
    Update the description of an Entity (Full Update).

    patch:
    Update the description of an Entity (Partial Update).
    """
    # pylint: disable=no-member
    queryset = Entity.objects.all()
    permission_classes = (AllowParticularEntityHead,)
    serializer_class = EntityDetailSerializer

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'entity': self.get_object()
        }


class ClubDetailWorkshopView(generics.RetrieveAPIView):
    """
    Get the Active and Past Workshop details of a Club
    """
    # pylint: disable=no-member
    queryset = Club.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = ClubDetailWorkshopSerializer

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()


class EntityDetailWorkshopView(generics.RetrieveAPIView):
    """
    Get the Active and Past Workshop details of an Entity
    """
    # pylint: disable=no-member
    queryset = Entity.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = EntityDetailWorkshopSerializer

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()


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
            'club': self.get_object()
        }

    # pylint: disable=unused-argument
    def get(self, *args, **kwargs):
        """
        Toggles the Club Subscription for current user.
        """
        serializer = self.get_serializer()
        serializer.toggle_subscription()
        return Response(status=status.HTTP_200_OK)


class EntitySubscriptionToggleView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = EntitySubscriptionToggleSerializer
    lookup_field = 'pk'
    # pylint: disable=no-member
    queryset = Entity.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'entity': self.get_object()
        }

    # pylint: disable=unused-argument
    def get(self, *args, **kwargs):
        """
        Toggles the Entity Subscription for current user.
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


class EntityView(generics.ListAPIView):
    """
    Get the Name and Image URL of all Entities.
    """
    # pylint: disable=no-member
    queryset = Entity.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = EntitySerializer


class CouncilDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
    Get the Name, Description, Secretaries, Clubs and Image URL of a Council.

    put:
    Update the description of a Council (Full Update).

    patch:
    Update the description of a Council (Partial Update).
    """
    # pylint: disable=no-member
    queryset = Council.objects.all()
    permission_classes = (AllowParticularCouncilHead,)
    serializer_class = CouncilDetailSerializer


class ClubTagCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowAnyClubHeadOrContact,)
    serializer_class = ClubTagCreateSerializer
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
            'club': self.get_object(),
        }

    # pylint: disable=unused-argument
    def post(self, request, pk):
        """
        Create Tag for a Club - only Club POR Holders or\
        any Workshop Contact are allowed to create a tag for the club.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()
        serializer = ClubTagCreateSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EntityTagCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowAnyEntityHeadOrContact,)
    serializer_class = EntityTagCreateSerializer
    lookup_field = 'pk'
    # pylint: disable=no-member
    queryset = Entity.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'entity': self.get_object(),
        }

    # pylint: disable=unused-argument
    def post(self, request, pk):
        """
        Create Tag for an Entity - only Entity Points of Contact or\
        any Workshop Contact are allowed to create a tag for the entity.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()
        serializer = EntityTagCreateSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClubTagDeleteView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowAnyClubHeadOrContact,)
    serializer_class = ClubTagDeleteSerializer
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
            'club': self.get_object(),
        }

    # pylint: disable=unused-argument
    def post(self, request, pk):
        """
        Delete Tag for a Club - only Club POR Holders or\
        any Workshop Contact are allowed to delete a tag for the club.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EntityTagDeleteView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowAnyEntityHeadOrContact,)
    serializer_class = EntityTagDeleteSerializer
    lookup_field = 'pk'
    # pylint: disable=no-member
    queryset = Entity.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'entity': self.get_object(),
        }

    # pylint: disable=unused-argument
    def post(self, request, pk):
        """
        Delete Tag for an Entity - only Entity POR Holders or\
        any Workshop Contact are allowed to delete a tag for the entity.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClubTagSearchView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ClubTagSearchSerializer
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
            'club': self.get_object(),
        }

    # pylint: disable=unused-argument
    def post(self, request, pk):
        """
        Search a Tag by tag name for a club
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tags = serializer.save()
        serializer = ClubTagSearchSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EntityTagSearchView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EntityTagSearchSerializer
    lookup_field = 'pk'
    # pylint: disable=no-member
    queryset = Entity.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'entity': self.get_object(),
        }

    # pylint: disable=unused-argument
    def post(self, request, pk):
        """
        Search a Tag by tag name for an Entity
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tags = serializer.save()
        serializer = EntityTagSearchSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkshopTagsUpdateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowWorkshopHeadOrContact,)
    serializer_class = WorkshopTagsUpdateSerializer
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
            'workshop': self.get_object()
        }

    # pylint: disable=unused-argument
    def put(self, request, pk):
        """
        Update the tags of a workshop. Only the Club POR Holders/Entity Points of Contact\
        or Workshop Contacts can perform this action.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


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
        Get all Workshops(both active and past) of both clubs and entities.
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
    Get the Active Workshops of clubs and entities
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopSerializer
    # pylint: disable=no-member
    queryset = Workshop.objects.filter(date__gte=date.today()).order_by('date', 'time')


class WorkshopPastView(generics.ListAPIView):
    """
    Get the Past Workshops of clubs and entities.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopSerializer
    # pylint: disable=no-member
    queryset = Workshop.objects.filter(date__lt=date.today()).order_by('-date', '-time')


class ClubWorkshopCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowAnyClubHead,)
    serializer_class = ClubWorkshopCreateSerializer
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
            'club': self.get_object(),
        }

    # pylint: disable=unused-argument
    def post(self, request, pk):
        """
        Create Workshops for a Club - only Club POR Holders are allowed to create a workshop.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workshop = serializer.save()
        serializer = ClubWorkshopCreateSerializer(workshop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EntityWorkshopCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowAnyEntityHead,)
    serializer_class = EntityWorkshopCreateSerializer
    lookup_field = 'pk'
    # pylint: disable=no-member
    queryset = Entity.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'entity': self.get_object(),
        }

    # pylint: disable=unused-argument
    def post(self, request, pk):
        """
        Create Workshops for an Entity - only Entity Points of Contact are allowed\
        to create a workshop.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workshop = serializer.save()
        serializer = EntityWorkshopCreateSerializer(workshop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WorkshopDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Get the title, description, club/entity, date, time, location, audience, resources, contacts\
    and image URL for a workshop.
    Also, get the number of interested users for the workshop\
    and whether the user is interested for the workshop.

    put:
    Update the title, description, date, time, location, audience and resources of a workshop.
    Only the Club POR Holders/Entity Points of Contact\
    and Workshop Contacts can update this. (Full Update)

    patch:
    Update the title, description, date, time, location, audience and resources of a workshop.
    Only the Club POR Holders/Entity Points of Contact\
    and Workshop Contacts can update this. (Partial Update)

    delete:
    Delete the workshop. Only the Club POR Holders/Entity Points of Contact\
    and Workshop Contacts can perform \
    this action.
    """
    permission_classes = (AllowWorkshopHeadOrContact,)
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
            'workshop': self.get_object()
        }

    # pylint: disable=unused-argument
    def put(self, request, pk):
        """
        Update the contacts of a workshop. Only the Club POR Holders/Entity Points of Contact \
        can perform this action.
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
            'workshop': self.get_object()
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
    Show all the club/entity workshops in which the user is interested.
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
        Search a club/entity workshop based on Title, Location or Audience.
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
        Search a club/entity workshop between the Start Date and End Date.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workshops = serializer.save()
        serializer = WorkshopSerializer(workshops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkshopResourceCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowWorkshopHeadOrContact,)
    serializer_class = WorkshopResourceSerializer
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
            'workshop': self.get_object()
        }

    # pylint: disable=unused-argument
    def post(self, request, pk):
        """
        Add a resource to a workshop with given id.\
        Only Club/Entity POR Holder or Workshop Contact can perform this action.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resource = serializer.add_resource()
        serialized_response = WorkshopResourceSerializer(instance=resource)
        return Response(serialized_response.data, status=status.HTTP_200_OK)


class WorkshopResourceView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Get the resource of a workshop, with particular resource id.

    put:
    Update the resource of a workshop, with particular resource id..
    Only the Club POR Holders/Entity Points of Contact\
    and Workshop Contacts can update this. (Full Update)

    patch:
    Update the resource of a workshop, with particular resource id..
    Only the Club POR Holders/Entity Points of Contact\
    and Workshop Contacts can update this. (Partial Update)

    delete:
    Delete the workshop resource.\
    Only the Club POR Holders/Entity Points of Contact\
    and Workshop Contacts can perform this action.
    """
    permission_classes = (AllowWorkshopHeadOrContactForResource, )
    serializer_class = WorkshopResourceSerializer
    # pylint: disable=no-member
    queryset = WorkshopResource.objects.all()


class ClubTagsView(generics.RetrieveAPIView):
    """
    Get list of tags of a particular club
    """
    # pylint: disable=no-member
    queryset = Club.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = ClubTagsSerializer


class EntityTagsView(generics.RetrieveAPIView):
    """
    Get list of tags of a particular entity.
    """
    # pylint: disable=no-member
    queryset = Entity.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = EntityTagsSerializer
