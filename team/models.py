from django.db import models

class Role(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True,
                             blank=True, related_name='team_members')
    github_username = models.CharField(max_length=50)
    github_image_url = models.URLField(null=True, blank=True, editable=False)

    def __str__(self):
        return f'{self.name} - {self.role}'
