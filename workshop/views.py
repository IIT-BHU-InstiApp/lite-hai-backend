from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import *


class CouncilView(generics.ListAPIView):
    queryset = Council.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CouncilSerializer


class CouncilDetailView(generics.RetrieveAPIView):
    queryset = Council.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CouncilDetailSerializer


class ClubDetailView(generics.RetrieveAPIView):
    queryset = Club.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = ClubDetailSerializer


class WorkshopView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopSerializer
    queryset = Workshop.objects.filter(date__gte=date.today()).order_by('date', 'time')


class WorkshopPastView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WorkshopSerializer
    queryset = Workshop.objects.filter(date__lt=date.today()).order_by('-date', '-time')


class WorkshopCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowAdmin,)
    serializer_class = WorkshopCreateSerializer

    def post(self, request):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.serializer.save()
        return Response(status=status.HTTP_200_OK)


class WorkshopDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowClubAdmin,)
    serializer_class = WorkshopDetailSerializer
    queryset = Workshop.objects.all()