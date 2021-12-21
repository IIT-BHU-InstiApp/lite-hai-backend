from rest_framework import generics
from .models import NoticeBoard
from .serializers import NoticeDetailSerializer, NoticeCreateSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .permissions import AllowNoticeContact


class NoticeListView(generics.ListAPIView):
    """
    Get All Notices
    """

    queryset = (
        # pylint: disable=no-member
        NoticeBoard.objects.all()
        .extra(select={"offset": "upvotes - downvotes"})
        .order_by("-offset")
    )
    permission_classes = (permissions.AllowAny,)
    serializer_class = NoticeDetailSerializer


class NoticeUpvoteView(generics.GenericAPIView):
    """
    Upvotes a notice
    """
    # pylint: disable=no-member
    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoticeDetailSerializer

    def get(self, request, pk):
        notice = self.queryset.get(id=pk)
        if notice is not None:
            if notice.voters.filter(username=request.user.username).first() is not None:
                return Response(
                    {"Error": "You can vote only once"}, status=status.HTTP_208_ALREADY_REPORTED
                )
            notice.upvotes += 1
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
    # pylint: disable=no-member
    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoticeDetailSerializer

    def get(self, request, pk):
        notice = self.queryset.get(id=pk)
        if notice is not None:
            if notice.voters.filter(username=request.user.username).first() is not None:
                return Response(
                    {"Error": "You can vote only once"}, status=status.HTTP_208_ALREADY_REPORTED
                )
            notice.downvotes += 1
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
