from rest_framework import generics, permissions ,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from authentication.models import UserProfile
from .models import ParliamentContact, ParliamentUpdate, ParliamentSuggestion
from .permissions import AllowParliamentHead
from .serializers import (
    ParliamentContactListSerializer, ParliamentContactDetailSerializer,
    ParliamentContactCreateSerializer, ParliamentUpdateListSerializer,
    ParliamentUpdateDetailSerializer, ParliamentUpdateCreateSerializer,
    SuggestionsSerializer,SuggestionCreateSerializer
    )

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
    Get All ParliamentUpdates
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
    Create New ParliamentUpdate 
    """
    # pylint: disable=no-member
    queryset = ParliamentUpdate.objects.all()
    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead)
    serializer_class = ParliamentUpdateCreateSerializer

class ParliamentUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update and Delete a ParliamentUpdate
    """

    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead)
    serializer_class = ParliamentUpdateDetailSerializer
    # pylint: disable=no-member
    queryset = ParliamentUpdate.objects.all()


class ParliamentSuggestionsListView(generics.ListAPIView):
    """
    Get All suggestions
    """
    queryset = (
        # pylint: disable=no-member
        ParliamentSuggestion.objects.all()
        .order_by("-upvotes", "-date")
    )
    permission_classes = (permissions.AllowAny,)
    serializer_class = SuggestionsSerializer

class ParliamentSuggestionsCreateView(generics.CreateAPIView):
    """
    Create New suggestion
    """
    # pylint: disable=no-member
    queryset = ParliamentSuggestion.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SuggestionCreateSerializer

class ParliamentSuggestionDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SuggestionsSerializer

    def get_queryset(self):
        user = get_object_or_404(UserProfile,user=self.request.user)
        return ParliamentSuggestion.objects.filter(author=user)

class ParliamentSuggestionUpvoteView(generics.GenericAPIView):
    """
    Upvote a suggestion
    """
    # pylint: disable=no-member
    queryset = ParliamentSuggestion.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SuggestionsSerializer

    def get(self, request, pk):
        suggestion = get_object_or_404(self.queryset,id=pk)
        user = UserProfile.objects.get(user=request.user)
        if suggestion.voters.filter(id = user.id).exists():
            return Response(
                {"Error": "You can vote only once"}, status=status.HTTP_208_ALREADY_REPORTED
            )
        suggestion.upvotes += 1
        suggestion.voters.add(user)
        suggestion.save()
        return Response(
            {"Message": "Upvoted successfully"}, status=status.HTTP_200_OK
        )

class ParliamentSuggestionDownvoteView(generics.GenericAPIView):
    """
    Downvote a suggestion
    """
    # pylint: disable=no-member
    queryset = ParliamentSuggestion.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SuggestionsSerializer

    def get(self, request, pk):
        suggestion = get_object_or_404(self.queryset,id=pk)
        user = UserProfile.objects.get(user=request.user)

        if suggestion.voters.filter(id = user.id).exists():
            return Response(
                {"Error": "You can vote only once"}, status=status.HTTP_208_ALREADY_REPORTED
            )
        suggestion.downvotes += 1
        suggestion.voters.add(user)
        suggestion.save()
        return Response(
            {"Message": "Downvoted successfully"}, status=status.HTTP_200_OK
        )
