from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import (
    Bill, Mess, Hostel
)
from .serializers import (
    HostelListSerializer, MessCancelSerializer,
    MessDetailSerializer, MessBillSerializer
)

# Create your views here.


class HostelListView(GenericAPIView):
    """
    get:
    Returns a list of all hostels.
    """
    permission_classes = []
    queryset = Hostel.objects.all()
    serializer_class = HostelListSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessListView(GenericAPIView):
    """
    get:
    Returns a list of (id, name) of all mess in a hostel.
    """
    permission_classes = []
    serializer_class = MessDetailSerializer

    def get_queryset(self):
        id = self.kwargs.get('pk')
        hostel = Hostel.objects.filter(id=id).first()
        return Mess.objects.filter(hostel=hostel).all()

    def get(self, request, pk):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessDetailView(GenericAPIView):
    """
    get:
    Returns mess details with given id.
    """
    permission_classes = []
    serializer_class = MessDetailSerializer

    def get_queryset(self):
        id = self.kwargs.get('pk')
        return Mess.objects.filter(id=id).first()

    def get(self, request, pk):
        serializer = self.get_serializer(self.get_queryset())
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessBillView(GenericAPIView):
    """
    get:
    Returns bill details of the student with given mess id for given month.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessBillSerializer
    queryset = Bill.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'mess_id': self.kwargs.get('pk'),
            'month': self.kwargs.get('month')
        })
        return context

    def get(self, request, pk, month):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bill = serializer.get_bill_details()
        return Response(bill, status=status.HTTP_200_OK)


class MessCancelView(GenericAPIView):
    """
    put:
    Cancels the subscription of the student to the mess with given id.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessCancelSerializer
    queryset = Mess.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'mess_id': self.kwargs.get('pk')
        })
        return context

    def put(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.cancel_mess()
        return Response(status=status.HTTP_200_OK)
