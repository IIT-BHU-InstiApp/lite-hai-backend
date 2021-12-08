from django.db import models

class NoticeBoard(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    ping = models.BooleanField(default=False)
    link = models.URLField(null=True, blank=True)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name + ' - ' + self.description
