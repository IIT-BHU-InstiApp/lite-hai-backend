from rest_framework import generics
from .models import NoticeBoard
from .serializers import NoticeGetSerializer, NoticeCreateSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response


class NoticeGetView(generics.ListAPIView):
    """
    Get All Notices
    """

    queryset = (
        NoticeBoard.objects.all()
        .extra(select={"offset": "upvote - downvote"})
        .order_by("-offset")
    )
    permission_classes = (permissions.AllowAny,)
    serializer_class = NoticeGetSerializer


class NoticeVoteView(generics.GenericAPIView):
    """
    Put Votes of notices
    """

    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = NoticeCreateSerializer

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


class NoticeCreateView(generics.GenericAPIView):
    """
    Create New Notice
    """

    queryset = NoticeBoard.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = NoticeGetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"Message": "Created successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


class NoticeUpdateView(generics.GenericAPIView):
    """
    Update and Delete a Notice
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = NoticeGetSerializer
    queryset = NoticeBoard.objects.all()

    def put(self, request, pk):
        try:
            notice = self.queryset.get(id=pk)
            for key in request.data:
                if key == "title":
                    notice.name = request.data["title"]
                if key == "description":
                    notice.description = request.data["description"]
                if key == "date":
                    notice.date = request.data["date"]
                if key == "notice_url":
                    notice.date = request.data["notice_url"]
                if key == "pin":
                    if request.data["pin"] == "true":
                        notice.pin = True
                    elif request.data["pin"] == "false":
                        notice.pin = False

            notice.save()
            return Response(
                {"Message": "Updated successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {"Error": "Notice not found"}, status=status.HTTP_204_NO_CONTENT
            )

    def delete(self, request, pk):
        try:
            NoticeBoard.objects.get(id=pk).delete()
            return Response(
                {"Message": "Deleted successfully"}, status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"Error": "Notice not found"}, status=status.HTTP_204_NO_CONTENT
            )
