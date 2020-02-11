from django.db import models

# Create your models here.

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    github_username = models.CharField(max_length=50)
    github_image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
    