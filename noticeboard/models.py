from django.db import models
from authentication.models import UserProfile

class NoticeBoard(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    voters = models.ManyToManyField(UserProfile, blank=True)
    importance = models.IntegerField(default = 0)

    def __str__(self):
        # pylint: disable=no-member
        return self.title + " - " + str(self.date.strftime("%Y-%m-%d %H:%M:%S"))
