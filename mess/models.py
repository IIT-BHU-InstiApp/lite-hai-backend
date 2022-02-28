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

    class Meta:
        verbose_name_plural = "messes"

    def __str__(self):
        return self.name


class Bill(models.Model):
    MONTH = ((1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
             (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'))

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    mess = models.ForeignKey(Mess, on_delete=models.CASCADE)
    monthly_bill = models.IntegerField()
    extra_charges = models.IntegerField(default=0)
    month = models.IntegerField(choices=MONTH)

    def __str__(self):
        return '{} {}'.format(self.user_profile.name, self.mess.name)
