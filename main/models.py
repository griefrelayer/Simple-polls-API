from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Poll(models.Model):
    """
    Polls model
    """

    name = models.CharField(max_length=150)
    start_date = models.DateField(editable=False)
    end_date = models.DateField()
    description = models.CharField(max_length=800)


class Question(models.Model):
    """
    Question model
    """
    text = models.CharField(max_length=300)
    type = models.CharField(max_length=8)
    poll = models.ForeignKey(to=Poll, on_delete=models.CASCADE)


class Answers(models.Model):
    """
    Answers model
    """
    uuid = models.UUIDField(auto_created=True)
    answer = JSONField()
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)


