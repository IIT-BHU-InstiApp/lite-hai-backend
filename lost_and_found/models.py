from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model


class LostAndFound(models.Model):
    TYPE = (('Lost', "Lost"), ('Found', "Found"))
    YEAR = (('1st', "1st"), ('2nd', "2nd"),
            ('3rd', "3rd"), ('4th', "4th"), ('5th', "5th"))
    COURSE = (('B.Tech', "B.Tech"), ('IDD', "IDD"), ('M.Tech', "M.Tech"))
    BRANCH = (('Architecture', "Architecture"), ('Ceramic', "Ceramic"),
              ('Chemical', "Chemical"), ('Civil',
                                         "Civil"), ('Computer Science', "Computer Science"),
              ('Electrical', "Electrical"), ('Electronics',
                                             "Electronics"), ('Mechanical', "Mechanical"),
              ('Metallurgical', "Metallurgical"), ('Mining', "Mining"), ('Pharmaceutical', "Pharmaceutical"))

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, default=None)
    name = models.TextField(max_length=200, blank=False, null=True)
    branch = models.CharField(choices=BRANCH, null=True, max_length=200)
    course = models.CharField(choices=COURSE, null=True, max_length=200)
    year = models.CharField(choices=YEAR, null=True, max_length=200)
    type_of_lost_and_found = models.CharField(choices=TYPE, max_length=10)
    description = models.TextField(max_length=4000, blank=False, null=True)
    drive_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name + '[' + self.type_of_lost_and_found + ']'
