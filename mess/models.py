from django.db import models
from grievance.models import Complaint
from authentication.models import UserProfile


# Create your models here.
class Hostel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Mess(models.Model):
    name = models.CharField(max_length=200)
    menu = models.URLField(max_length=200)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Bill(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    mess = models.ForeignKey(Mess, on_delete=models.CASCADE)
    monthly_bill = models.IntegerField()
    extra_charges = models.IntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.user_profile.name, self.mess.name)
