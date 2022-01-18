from django.db import models
from authentication.models import UserProfile

# Model for Parliament Contact
class Contact(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50)

    def __str__(self):
        return self.profile.name + " - " + self.designation

# Model for Parliament Update
class Update(models.Model):
    title=models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="Update")
    date = models.DateTimeField(auto_now_add=True)
    upvotes=models.IntegerField(default=0)
    downvotes=models.IntegerField(default=0)
    voters=models.ManyToManyField(UserProfile, blank=True)

    def __str__(self):
        return self.title

# Model for Parliament Suggestion
class Suggestion(models.Model):
    title=models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="Suggestion")
    date = models.DateTimeField(auto_now_add=True)
    upvotes=models.IntegerField(default=0)
    downvotes=models.IntegerField(default=0)
    voters=models.ManyToManyField(UserProfile, blank=True)

    def __str__(self):
        return self.title

