from rest_framework import generics, permissions, status
from rest_framework.response import Response

from authentication.models import UserProfile
from .models import NoticeBoard
from .serializers import NoticeDetailSerializer, NoticeCreateSerializer, NoticeListSerializer
from .permissions import AllowNoticeContact


class NoticeListView(generics.ListAPIView):
    """
    Get All Notices
    """

    queryset = (
        # pylint: disable=no-member
        NoticeBoard.objects.all()
        .order_by("-importance", "-date")
    )
    permission_classes = (permissions.AllowAny,)
    serializer_class = NoticeListSerializer

class NoticeCreateView(generics.CreateAPIView):
    """
    Create New Notice
    """
    # pylint: disable=no-member
    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated, AllowNoticeContact)
    serializer_class = NoticeCreateSerializer

class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update and Delete a Notice
    """

    permission_classes = (permissions.IsAuthenticated, AllowNoticeContact)
    serializer_class = NoticeDetailSerializer
    # pylint: disable=no-member
    queryset = NoticeBoard.objects.all()

class NoticeUpvoteView(generics.GenericAPIView):
    """
    Upvotes a notice
    """
    # pylint: disable=no-member
    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoticeDetailSerializer

    def get(self, request, pk):
        """Check if already voted or not"""
        notice = self.queryset.get(id=pk)
        user = UserProfile.objects.get(user=request.user)
        if notice is not None:
            if notice.voters.filter(id = user.id).exists():
                return Response(
                    {"Error": "You can vote only once"}, status=status.HTTP_208_ALREADY_REPORTED
                )
            notice.upvotes += 1
            notice.voters.add(user)
            notice.save()
            return Response(
                {"Message": "Upvoted successfully"}, status=status.HTTP_200_OK
            )
        return Response(
                {"Error": "Notice not found"}, status=status.HTTP_204_NO_CONTENT
            )


class NoticeDownvoteView(generics.GenericAPIView):
    """
    Downvote a notice
    """
    # pylint: disable=no-member
    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoticeDetailSerializer

    def get(self, request, pk):
        """Check if already voted or not"""
        notice = self.queryset.get(id=pk)
        user = UserProfile.objects.get(user=request.user)
        if notice is not None:
            if notice.voters.filter(id = user.id).exists():
                return Response(
                    {"Error": "You can vote only once"}, status=status.HTTP_208_ALREADY_REPORTED
                )
            notice.downvotes += 1
            notice.voters.add(user)
            notice.save()
            return Response(
                {"Message": "Downvoted successfully"}, status=status.HTTP_200_OK
            )
        return Response(
                {"Error": "Notice not found"}, status=status.HTTP_204_NO_CONTENT
            )
