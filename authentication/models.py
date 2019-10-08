from django.db import models
from django.contrib.auth.models import User
from .utils import FirebaseAPI

# Create your models here.
class UserProfile(models.Model):
    uid = models.CharField(max_length=64, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=8)
    mobile_number = models.CharField(max_length=15)
    department = models.CharField(max_length=60)
    course = models.CharField(max_length=30)
    year_of_joining = models.CharField(max_length=4)

    def __str__(self):
        return self.name