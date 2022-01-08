from rest_framework import generics, permissions
from .models import ParliamentContact, ParliamentUpdate
from .permissions import AllowParliamentHead
from .serializers import (
    ParliamentContactListSerializer, ParliamentContactDetailSerializer,
    ParliamentContactCreateSerializer, ParliamentUpdateListSerializer,
    ParliamentUpdateDetailSerializer, ParliamentUpdateCreateSerializer)

class ParliamentContactListView(generics.ListAPIView):
    """
    Get All Parliament Contacts
    """

    queryset = ParliamentContact.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = ParliamentContactListSerializer

class ParliamentContactCreateView(generics.CreateAPIView):
    """
    Create New Parliament Contact
    """
    # pylint: disable=no-member
    queryset = ParliamentContact.objects.all()
    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead)
    serializer_class = ParliamentContactCreateSerializer

class ParliamentContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update and Delete a Parliament Contact
    """

    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead)
    serializer_class = ParliamentContactDetailSerializer
    # pylint: disable=no-member
    queryset = ParliamentContact.objects.all()

class ParliamentUpdateListView(generics.ListAPIView):
    """
    Get All Notices
    """

    queryset = (
        # pylint: disable=no-member
        ParliamentUpdate.objects.all()
        .order_by("-importance", "-date")
    )
    permission_classes = (permissions.AllowAny,)
    serializer_class = ParliamentUpdateListSerializer

class ParliamentUpdateCreateView(generics.CreateAPIView):
    """
    Create New Notice
    """
    # pylint: disable=no-member
    queryset = ParliamentUpdate.objects.all()
    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead)
    serializer_class = ParliamentUpdateCreateSerializer

class ParliamentUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update and Delete a Notice
    """

    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead)
    serializer_class = ParliamentUpdateDetailSerializer
    # pylint: disable=no-member
    queryset = ParliamentUpdate.objects.all()
