from django.db import models
from django.contrib.auth.models import User
from .utils import FirebaseAPI

# Create your models here.
class UserProfile(models.Model):
    uid = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    department = models.CharField(max_length=60)
    year_of_joining = models.CharField(max_length=10)

    def __str__(self):
        return self.name
