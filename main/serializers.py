from rest_framework.serializers import ModelSerializer
from .models import Poll, Question, Answer


class PollDefaultSerializer(ModelSerializer):
    """
    This serializer serializes Poll object with all fields
    """
    class Meta:
        fields = "__all__"
        model = Poll


class PollUpdateSerializer(ModelSerializer):
    """
    This serializer serializes Poll object for updating without start_date
    (as this field shouldn't be edited after poll creation)
    """
    class Meta:
        exclude = ["start_date"]
        model = Poll


class QuestionSerializer(ModelSerializer):
    """
    This serializer serializes Question object with all fields
    """
    class Meta:
        fields = "__all__"
        model = Question


class AnswerSerializer(ModelSerializer):
    """
    This serializer serializes Answer object with all fields
    """
    class Meta:
        fields = "__all__"
        model = Answer
