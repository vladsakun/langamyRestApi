from django.conf import settings
from django.db import models


class StudySets(models.Model):
    name = models.CharField(max_length=256)
    words = models.TextField()
    creator = models.EmailField()
    percent_of_studying = models.IntegerField(blank=True, null=True)
    studied = models.BooleanField(default=False)
    amount_of_words = models.IntegerField()

    def __str__(self):
        return '%s %s' % (self.name, self.creator)


# Create your models here.
