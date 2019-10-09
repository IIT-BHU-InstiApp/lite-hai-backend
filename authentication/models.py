from django.db import models
from django.contrib.auth.models import User
from .utils import FirebaseAPI

# Create your models here.
class UserProfile(models.Model):
    uid = models.CharField(max_length=64, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    roll_number = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=15)
    department = models.CharField(max_length=60)
    course = models.CharField(max_length=40)
    year_of_joining = models.CharField(max_length=10)

    def __str__(self):
        return self.name
