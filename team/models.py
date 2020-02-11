from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    github_username = models.CharField(max_length=50)
    github_image_url = models.URLField(null=True, blank=True, editable=False)

    def __str__(self):
        return self.name
    