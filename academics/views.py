from rest_framework import generics, permissions, status
from rest_framework.response import Response
from authentication.models import UserProfile
from .models import AcademicSchedule, StudyMaterials, ProffsAndHODs
from .serializers import (AcademicScheduleSerializer,
                          ProffsAndHODsSerializer, StudyMaterialsSerializer)
from authentication.models import UserProfile
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class AcademicScheduleView(generics.RetrieveUpdateAPIView):
    """
    get:
    Get the academic schedule of the branch and year

    put:
    Update the academic schedule (Full update)

    patch:
    Update the academic schedule (Partial update)
    """
    # pylint: disable=no-member
    queryset = AcademicSchedule.objects.all()
    serializer_class = AcademicScheduleSerializer

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [IsAuthenticated()]
    #     else:
    #         return[IsAdminUser()]

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        if hasattr(self, 'obj'):
            return self.obj
        obj = super().get_object()
        setattr(self, 'obj', obj)
        return obj


class StudyMaterialsView(generics.ListAPIView):
    queryset = StudyMaterials.objects.all()
    serializer_class = StudyMaterialsSerializer


class ProffsAndHODsView(generics.RetrieveAPIView):
    '''
    Accepts a parameter dept and returns a url of the professors of the given department.
    'dept' is the acronym of the department same as in the email id and contains lower case letters only.
    '''

    queryset = ProffsAndHODs.objects.all()
    serializer_class = ProffsAndHODsSerializer
    lookup_field = 'department'
    lookup_url_kwarg = 'dept'
