from rest_framework import generics
from .models import NoticeBoard
from .serializers import NoticeGetSerializer, NoticeCreateSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .permissions import AllowNoticeContact
from authentication.models import UserProfile


class NoticeGetView(generics.ListAPIView):
    """
    Get All Notices
    """

    queryset = (
        NoticeBoard.objects.all()
        .extra(select={"offset": "upvote - downvote"})
        .order_by("-offset")
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoticeGetSerializer


class NoticeUpvoteView(generics.GenericAPIView):
    """
    Upvotes a notice
    """

    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoticeGetSerializer

    def get(self, request, pk):
        notice = self.queryset.get(id=pk)
        if notice is not None:
            if notice.voters.filter(username=request.user.username).first() is not None:
                return Response(
                    {"Error": "You can vote only once"}, status=status.HTTP_208_ALREADY_REPORTED
                )
            notice.upvote += 1
            notice.voters.add(request.user)
            notice.save()
            return Response(
                {"Message": "Updated successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"Error": "Notice not found"}, status=status.HTTP_204_NO_CONTENT
            )


class NoticeDownvoteView(generics.GenericAPIView):
    """
    Downvote a notice
    """

    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoticeGetSerializer

    def get(self, request, pk):
        notice = self.queryset.get(id=pk)
        if notice is not None:
            if notice.voters.filter(username=request.user.username).first() is not None:
                return Response(
                    {"Error": "You can vote only once"}, status=status.HTTP_208_ALREADY_REPORTED
                )
            notice.downvote += 1
            notice.voters.add(request.user)
            notice.save()
            return Response(
                {"Message": "Updated successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"Error": "Notice not found"}, status=status.HTTP_204_NO_CONTENT
            )


class NoticeCreateView(generics.CreateAPIView):
    """
    Create New Notice
    """

    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated, AllowNoticeContact)
    serializer_class = NoticeCreateSerializer


class NoticeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update and Delete a Notice
    """

    permission_classes = (permissions.IsAuthenticated, AllowNoticeContact)
    serializer_class = NoticeGetSerializer
    queryset = NoticeBoard.objects.all()
