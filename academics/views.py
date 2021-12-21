from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import AcademicSchedule, StudyMaterials, ProfsAndHODs
from .serializers import (AcademicScheduleSerializer,
                          ProfsAndHODsSerializer, StudyMaterialsSerializer)


class AcademicScheduleView(generics.RetrieveAPIView):
    """
    Returns the academic schedule of the branch and year.
    Takes two parameters department and year of joining
    """
    # pylint: disable=no-member
    queryset = AcademicSchedule.objects.all()
    serializer_class = AcademicScheduleSerializer

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        department = self.kwargs.get('dept')
        year_of_joining = self.kwargs.get('year')
        obj = get_object_or_404(
            self.get_queryset(), department=department, year_of_joining=year_of_joining)
        return obj


class StudyMaterialsView(generics.RetrieveAPIView):
    '''
    Accepts a parameter dept and returns a url of the study materials for the given department.
    'dept' is the acronym of the department same as in the email id and contains lower case letters
    only.
    '''
    # pylint: disable=no-member
    queryset = StudyMaterials.objects.all()
    serializer_class = StudyMaterialsSerializer
    lookup_field = 'department'
    lookup_url_kwarg = 'dept'


class ProfsAndHODsView(generics.RetrieveAPIView):
    '''
    Accepts a parameter dept and returns a url of the professors of the given department.
    'dept' is the acronym of the department same as in the email id and contains lower case letters
    only.
    '''
    # pylint: disable=no-member
    queryset = ProfsAndHODs.objects.all()
    serializer_class = ProfsAndHODsSerializer
    lookup_field = 'department'
    lookup_url_kwarg = 'dept'
