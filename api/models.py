import uuid

from django.conf import settings
from django.db import models


class User(models.Model):
    email = models.CharField(max_length=256)
    marks = models.TextField(default="", blank=True)

    def __str__(self):
        return self.email


class StudySets(models.Model):
    name = models.CharField(max_length=256)
    language_to = models.CharField(max_length=256)
    language_from = models.CharField(max_length=256)
    words = models.TextField()
    creator = models.EmailField()
    percent_of_studying = models.IntegerField(blank=True, null=True)
    studied = models.BooleanField(default=False)
    amount_of_words = models.IntegerField()

    def __str__(self):
        return '%s %s' % (self.name, self.creator)


class Dictation(models.Model):
    code = models.IntegerField(null=True, unique=True)
    name = models.CharField(max_length=256, default="Dictation")
    creator = models.EmailField()
    words = models.TextField()
    marked_words = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name="members", through="DictationMark")
    type_of_questions = models.CharField(max_length=256, default="quiz")
    amount_of_words = models.IntegerField(default=2)
    amount_of_words_for_dictation = models.IntegerField(default=2)

    def __str__(self):
        return '%s %s' % (self.code, self.creator)


class DictationMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dictation = models.ForeignKey(Dictation, on_delete=models.CASCADE)
    mark = models.IntegerField()

    def __str__(self):
        return '%s %s' % (self.user.email, self.dictation.code)
