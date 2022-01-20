from rest_framework import generics, permissions ,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from authentication.models import UserProfile
from .models import Contact, Update, Suggestion
from .permissions import AllowParliamentHead
from noticeboard.permissions import AllowNoticeContact
from .serializers import (
    ContactsSerializer, ContactCreateSerializer,
    UpdatesSerializer, UpdateCreateSerializer,
    SuggestionsSerializer,SuggestionCreateSerializer
    )

class ContactsListView(generics.ListAPIView):
    """
    Get All Parliament Contacts
    """
    queryset = Contact.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = ContactsSerializer

class ContactsCreateView(generics.CreateAPIView):
    """
    Create New Parliament Contact
    """
    # pylint: disable=no-member
    queryset = Contact.objects.all()
    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead,)
    serializer_class = ContactCreateSerializer

class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update and Delete a Parliament Contact
    """
    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead,)
    serializer_class = ContactsSerializer
    # pylint: disable=no-member
    queryset = Contact.objects.all()

class UpdatesListView(generics.ListAPIView):
    """
    Get All Parliament Updates
    """
    queryset = (
        # pylint: disable=no-member
        Update.objects.all()
        .order_by("-upvotes", "-date")
    )
    permission_classes = (permissions.AllowAny,)
    serializer_class = UpdatesSerializer

class UpdatesCreateView(generics.CreateAPIView):
    """
    Create New Parliament Update
    """
    # pylint: disable=no-member
    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead | AllowNoticeContact,)
    queryset = Update.objects.all()
    serializer_class = UpdateCreateSerializer

    def perform_create(self, serializer):
        user = get_object_or_404(UserProfile,user=self.request.user)
        serializer.save(author=user)


class UpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update and Delete a Parliament Update
    """
    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead | AllowNoticeContact,)
    serializer_class = UpdatesSerializer

    def get_queryset(self):
        if(self.request.user.is_authenticated):
            user = get_object_or_404(UserProfile,user=self.request.user)
            return Update.objects.filter(author=user)
        return

class UpdateUpvoteView(generics.GenericAPIView):
    """
    Upvote a Parliament Update
    """
    # pylint: disable=no-member
    queryset = Update.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdatesSerializer

    def get(self, request, pk):
        update = get_object_or_404(self.queryset,id=pk)
        user = UserProfile.objects.get(user=request.user)
        if update.voters.filter(id = user.id).exists():
            return Response(
                {"Error": "You can vote only once"}, status=status.HTTP_208_ALREADY_REPORTED
            )
        update.upvotes += 1
        update.voters.add(user)
        update.save()
        return Response(
            {"Message": "Upvoted successfully"}, status=status.HTTP_200_OK
        )

class UpdateDownvoteView(generics.GenericAPIView):
    """
    Downvote a Parliament Update
    """
    # pylint: disable=no-member
    queryset = Update.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdatesSerializer

    def get(self, request, pk):
        update = get_object_or_404(self.queryset,id=pk)
        user = UserProfile.objects.get(user=request.user)

        if update.voters.filter(id = user.id).exists():
            return Response(
                {"Error": "You can vote only once"}, status=status.HTTP_208_ALREADY_REPORTED
            )
        update.downvotes += 1
        update.voters.add(user)
        update.save()
        return Response(
            {"Message": "Downvoted successfully"}, status=status.HTTP_200_OK
        )

class SuggestionsListView(generics.ListAPIView):
    """
    Get All Parliament Suggestions
    """
    queryset = (
        # pylint: disable=no-member
        Suggestion.objects.all()
        .order_by("-upvotes", "-date")
    )
    permission_classes = (permissions.AllowAny,)
    serializer_class = SuggestionsSerializer

class SuggestionsCreateView(generics.CreateAPIView):
    """
    Create New Parliament Suggestion
    """
    # pylint: disable=no-member
    permission_classes = (permissions.IsAuthenticated, AllowParliamentHead,)
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionCreateSerializer

    def perform_create(self, serializer):
        user = get_object_or_404(UserProfile,user=self.request.user)
        serializer.save(author=user)


class SuggestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update or Delete a Parliament Suggestion
    """
    serializer_class = SuggestionsSerializer

    def get_permissions(self):
        if(self.request.method == 'GET'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


    def get_queryset(self):
        if (self.request.method=='GET'):
            return Suggestion.objects.all()
        if(self.request.user.is_authenticated):
            user = get_object_or_404(UserProfile,user=self.request.user)
            if(user.can_add_parliament_details or user.can_post_notice):
                return Suggestion.objects.all()
            return Suggestion.objects.filter(author=user)
        return Response(
            {"Message": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED
        )


class SuggestionUpvoteView(generics.GenericAPIView):
    """
    Upvote a Parliament Suggestion
    """
    # pylint: disable=no-member
    queryset = Suggestion.objects.all()
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

class SuggestionDownvoteView(generics.GenericAPIView):
    """
    Downvote a Parliament Suggestion
    """
    # pylint: disable=no-member
    queryset = Suggestion.objects.all()
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
