from django.db import models
from authentication.models import UserProfile

class ParliamentContact(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50)

    def __str__(self):
        return self.name.user.username + " - " + self.designation

class ParliamentUpdate(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    importance = models.IntegerField(default = 0)

    def __str__(self):
        return self.title

