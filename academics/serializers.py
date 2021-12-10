from rest_framework import serializers
from rest_framework.exceptions import NotFound
from drf_yasg2.utils import swagger_serializer_method
from .models import AcademicSchedule, ProffsAndHODs, StudyMaterials


class AcademicScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSchedule
        fields = ('department', 'year_of_joining', 'schedule_url',)


class StudyMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterials
        fields = ('resource_url',)


class ProffsAndHODsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProffsAndHODs
        fields = ('department', 'proffs_and_HODs')
