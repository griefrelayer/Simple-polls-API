from rest_framework.serializers import ModelSerializer
from .models import Poll, Question, Answer


class PollDefaultSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Poll


class PollUpdateSerializer(ModelSerializer):
    class Meta:
        exclude = ["start_date"]
        model = Poll


class QuestionSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Question


class AnswerSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Answer
