from django.db import models
from django.contrib.auth import get_user_model
from authentication.models import UserProfile


class NoticeBoard(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    notice_contact = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notice_contact",
    )
    notice_url = models.URLField(null=True, blank=True)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    voters = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        return self.title + " - " + self.description
