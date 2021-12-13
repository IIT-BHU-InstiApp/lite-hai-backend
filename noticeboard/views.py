from rest_framework import generics
from .models import NoticeBoard
from .serializers import NoticeGetSerializer, NoticeCreateSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .permissions import AllowNoticeContact

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


class NoticeVoteView(generics.GenericAPIView):
    """
    Put Votes of notices
    """

    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoticeGetSerializer

    def put(self, request, pk):
        try:
            notice = self.queryset.get(id=pk)
            if request.data["vote"] == "D":
                notice.downvote += 1
            elif request.data["vote"] == "U":
                notice.upvote += 1
            notice.save()
            return Response(
                {"Message": "Updated successfully"}, status=status.HTTP_200_OK
            )
        except:
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
