import re
from django.db import models
from django.core.exceptions import ValidationError
from authentication.models import UserProfile

def validate_kebab_case(string):
    """
    Validate whether the string is in kebab-case
    """
    pattern = re.compile(r"^[a-z0-9]+(\-[a-z0-9]+)*$")
    if not pattern.match(string):
        raise ValidationError(
            "The string must contain only dashes or lowercase english alphabets or digits")


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
    website_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.name


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
    website_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.name


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, validators=[validate_kebab_case])
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return f'{self.tag_name} - {self.club}'


class Workshop(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='workshops')
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=50)
    latitude = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    audience = models.CharField(blank=True, max_length=50)
    contacts = models.ManyToManyField(UserProfile, blank=True, related_name='organized_workshops')
    interested_users = models.ManyToManyField(UserProfile, blank=True,
                                              related_name='interested_workshops')
    image_url = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tagged_workshops')
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.title


class WorkshopResource(models.Model):
    RESOURCE_TYPES = [
        ('Prerequisite', 'Prerequisite'),
        ('Material', 'Material')
    ]
    name = models.CharField(max_length=50)
    link = models.URLField()
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE,
                                 related_name='resources')
    resource_type = models.CharField(choices=RESOURCE_TYPES, max_length=20)
