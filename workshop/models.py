from django.db import models
from authentication.models import *


class Council(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    secy = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='council_secy')
    joint_secy = models.ManyToManyField(UserProfile, blank=True, related_name='council_joint_secy')

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    council = models.ForeignKey(Council, on_delete=models.CASCADE, related_name='clubs')
    secy = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='club_secy')
    joint_secy = models.ManyToManyField(UserProfile, blank=True, related_name='club_joint_secy')

    def __str__(self):
        return f'{self.name} - {self.council.name}'


class Workshop(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='workshops')
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=50)
    audience = models.CharField(blank=True, max_length=50)
    resources = models.TextField(null=True, blank=True)
    contacts = models.ManyToManyField(UserProfile, blank=True, related_name='workshop_contact')

    def __str__(self):
        return f'{self.title} on {self.date} - {self.club.name}'