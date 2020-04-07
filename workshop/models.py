from django.db import models
from authentication.models import UserProfile


class Council(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    gensec = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='council_gensec', verbose_name='General Secretary')
    joint_gensec = models.ManyToManyField(UserProfile, blank=True,
                                          related_name='council_joint_gensec',
                                          verbose_name='Joint General Secretary')
    small_image_url = models.URLField(null=True, blank=True)
    large_image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    council = models.ForeignKey(Council, on_delete=models.CASCADE, related_name='clubs')
    secy = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True,
                             blank=True, related_name='club_secy', verbose_name='Secretary')
    joint_secy = models.ManyToManyField(UserProfile, blank=True, related_name='club_joint_secy',
                                        verbose_name='Joint Secretary')
    subscribed_users = models.ManyToManyField(UserProfile, blank=True, related_name='subscriptions')
    small_image_url = models.URLField(null=True, blank=True)
    large_image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Workshop(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='workshops')
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=50)
    audience = models.CharField(blank=True, max_length=50)
    resources = models.TextField(null=True, blank=True)
    contacts = models.ManyToManyField(UserProfile, blank=True, related_name='organized_workshops')
    attendees = models.ManyToManyField(UserProfile, blank=True, related_name='attended_workshops')
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
