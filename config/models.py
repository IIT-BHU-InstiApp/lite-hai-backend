from django.db import models

class ConfigVar(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()

    def __str__(self):
        return '%s' % self.name
