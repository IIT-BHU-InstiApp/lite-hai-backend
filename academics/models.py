# pylint: disable=too-few-public-methods
from django.db import models

# Create your models here.

dept_list = (
    ('bce', 'Biochemical Engineering'),
    ('bme', 'Biomedical Engineering'),
    ('cer', 'Ceramic Engineering'),
    ('che', 'Chemical Engineering'),
    ('chy', 'Chemistry'),
    ('civ', 'Civil Engineering'),
    ('cse', 'Computer Science and Engineering'),
    ('ece', 'Electronics Engineering'),
    ('eee', 'Electrical Engineering'),
    ('mat', 'Mathematics and Computing'),
    ('mec', 'Mechanical Engineering'),
    ('met', 'Metallurgical Engineering'),
    ('min', 'Mining Engineering'),
    ('mst', 'Materials Science and Technology'),
    ('phe', 'Pharmaceutical Engineering and Technology'),
    ('phy', 'Physics'),
    ('hss', 'Humanistic Studies'),
)


class AcademicSchedule(models.Model):
    department = models.CharField(max_length=60, choices=dept_list)
    year_of_joining = models.CharField(max_length=10)
    schedule_url = models.URLField()

    def __str__(self):
        return f"{self.department} {self.year_of_joining} Academic schedule"


class StudyMaterials(models.Model):
    department = models.CharField(max_length=60, choices=dept_list)
    resource_url = models.URLField()

    class Meta:
        verbose_name_plural = 'Study Materials'

    def __str__(self):
        return f"{self.department} resources"


class ProfsAndHODs(models.Model):
    department = models.CharField(max_length=60)
    profs_and_HODs = models.URLField(default='https://www.iitbhu.ac.in/dept')

    class Meta:
        verbose_name = 'Profs and HODs'
        verbose_name_plural = 'Profs and HODs'

    def __str__(self):
        return f"{self.department} Professors"
