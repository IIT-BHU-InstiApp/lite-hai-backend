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
        return f'{self.name}'


class Club(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    council = models.ForeignKey(Council, on_delete=models.CASCADE, related_name='clubs')
    secy = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True,
                             blank=True, related_name='club_secy', verbose_name='Secretary')
    joint_secy = models.ManyToManyField(UserProfile, blank=True, related_name='club_joint_secy',
                                        verbose_name='Joint Secretary')
    subscribed_users = models.ManyToManyField(UserProfile, blank=True,
                                        related_name='club_subscriptions')
    small_image_url = models.URLField(null=True, blank=True)
    large_image_url = models.URLField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Entity(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    is_permanent = models.BooleanField(default = False)
    is_highlighted = models.BooleanField(default = False)
    point_of_contact = models.ManyToManyField(UserProfile, blank=True,
                                        related_name='entity_point_of_contact',
                                        verbose_name='Point of Contact')
    subscribed_users = models.ManyToManyField(UserProfile, blank=True,
                                              related_name='entity_subscriptions')
    small_image_url = models.URLField(null=True, blank=True)
    large_image_url = models.URLField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['tag_name', 'club']),
            models.Index(fields=['tag_name', 'entity']),
            models.Index(fields=['club']),
            models.Index(fields=['entity'])]
    tag_name = models.CharField(
        max_length=50, validators=[validate_kebab_case])
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='tags',
                             blank = True,  null = True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='entity_tags',
                                blank = True, null = True)

    def __str__(self):
        return f'{self.tag_name}'


class Workshop(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['date', 'time']),
            models.Index(fields=['-date', '-time']),
            models.Index(fields=['club', '-date']),
            models.Index(fields=['club', 'date']),
            models.Index(fields=['title']),
            models.Index(fields=['location']),
            models.Index(fields=['audience']),
        ]
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='entity_workshops',
                               blank=True, null = True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='workshops',
                             blank=True, null = True)
    is_workshop = models.BooleanField(default=True) # True if it is a workshop, False for an event
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=100)
    latitude = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    audience = models.CharField(blank=True, max_length=100)
    contacts = models.ManyToManyField(UserProfile, blank=True, related_name='organized_workshops')
    interested_users = models.ManyToManyField(UserProfile, blank=True,
                                              related_name='interested_workshops')
    image_url = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tagged_workshops')
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class WorkshopResource(models.Model):
    RESOURCE_TYPES = [
        ('Prerequisite', 'Prerequisite'),
        ('Material', 'Material')
    ]
    name = models.CharField(max_length=100)
    link = models.URLField()
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE,
                                 related_name='resources')
    resource_type = models.CharField(choices=RESOURCE_TYPES, max_length=20)
