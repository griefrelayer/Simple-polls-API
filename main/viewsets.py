from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, SAFE_METHODS
from rest_framework.decorators import action
from .models import Poll, Question, Answer
from .serializers import PollDefaultSerializer, PollUpdateSerializer, QuestionSerializer, AnswerSerializer

from datetime import datetime


class PollViewSet(ModelViewSet):
    """
    API endpoint that allows Poll objects creating, updating, deleting, listing and detail view.
    For the admins, all actions are allowed, for others only list and detail view are allowed.
    """
    model = Poll
    serializer_class = PollDefaultSerializer

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return [IsAdminUser()]
        else:
            return [DjangoModelPermissionsOrAnonReadOnly()]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Poll.objects.all()
        else:
            current_date = datetime.date(datetime.now())
            return Poll.objects.filter(start_date__lt=current_date, end_date__gt=current_date)

    def update(self, request, *args, **kwargs):
        self.serializer_class = PollUpdateSerializer
        super().update(request, *args, **kwargs)


class QuestionViewSet(ModelViewSet):
    """
    API endpoint that allows Question objects creating, updating, deleting, list and detail view.
    Also it allows Answer object creation
    For the admins, all actions are allowed, for others only list, detail view and answer are allowed.
    answer action is allowing users to create answers
    """
    model = Question
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action == 'answer':
            return [AllowAny()]
        elif self.request.method not in SAFE_METHODS:
            return [IsAdminUser()]
        else:
            return [DjangoModelPermissionsOrAnonReadOnly()]

    def get_queryset(self):
        return Question.objects.filter(poll=self.kwargs.get('polls_pk', 1))

    @action(methods=['post'], detail=True)
    def answer(self, request, *args, **kwargs):
        self.serializer_class = AnswerSerializer
        request.data._mutable = True
        request.data['question'] = kwargs['pk']
        request.data._mutable = False
        return super().create(request, *args, **kwargs)


class AnsweredPollsView(APIView):
    """
    API endpoint that allows to view list of answered polls by provided user_id
    """
    permission_classes = [AllowAny]
    serializer_class = PollDefaultSerializer

    def get(self, request, format=None, pk=None):
        answers = Answer.objects.filter(anonuser_id=pk)
        questions = [ans.question for ans in answers]
        polls = [q.poll for q in questions]
        return Response(PollDefaultSerializer(polls, many=True).data)


class AnsweredPollQuestionView(APIView):
    """
    API endpoint that allows to view list of answered questions in the poll by provided poll_id and user_id
    """
    permission_classes = [AllowAny]
    serializer_class = AnswerSerializer

    def get(self, request, format=None, pk=None, pk2=None):
        answers = Answer.objects.filter(anonuser_id=pk, question__poll_id=pk2)
        return Response(AnswerSerializer(answers, many=True).data)


