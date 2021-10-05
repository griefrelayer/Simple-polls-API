from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

'''for user in User.objects.all():
    Token.objects.get_or_create(user=user)'''
# Create your models here.


class Poll(models.Model):
    """
    Polls model
    """

    name = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=800)

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"


class Question(models.Model):
    """
    Question model
    """
    text = models.CharField(max_length=300)
    type = models.CharField(max_length=8)
    poll = models.ForeignKey(to=Poll, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    """
    Answer model
    """
    anonuser_id = models.IntegerField()
    answer = JSONField()
    question = models.OneToOneField(to=Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


