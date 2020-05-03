from django.db import models
import requests

def get_github_profile_pic_url(username):
    """
    Get the profile picture url from the github handle
    """
    r = requests.get('https://api.github.com/users/' + username)
    github_user_json = r.json()
    return github_user_json['avatar_url']

class Role(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % self.role


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True,
                             blank=True, related_name='team_members')
    github_username = models.CharField(max_length=50)
    github_image_url = models.URLField(null=True, blank=True, editable=False)

    # pylint: disable=arguments-differ, signature-differs
    def save(self, *args, **kwargs):
        self.github_image_url = get_github_profile_pic_url(self.github_username)
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.name
