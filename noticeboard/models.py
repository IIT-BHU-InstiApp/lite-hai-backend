from django.db import models


class NoticeBoard(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    pin = models.BooleanField(default=False)
    notice_url = models.URLField(null=True, blank=True)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    def __str__(self):
        return self.title + " - " + self.description
