from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, SAFE_METHODS
from rest_framework.decorators import action
from .models import Poll, Question, Answer
from .serializers import PollDefaultSerializer, PollUpdateSerializer, QuestionSerializer, AnswerSerializer

from datetime import datetime


class PollViewSet(ModelViewSet):
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
        return Question.objects.filter(poll=self.kwargs['polls_pk'])

    @action(methods=['post'], detail=True)
    def answer(self, request, *args, **kwargs):
        self.serializer_class = AnswerSerializer
        request.data._mutable = True
        request.data['question'] = kwargs['pk']
        request.data._mutable = False
        return super().create(request, *args, **kwargs)


class AnswerViewSet(ModelViewSet):
    model = Answer
    serializer_class = AnswerSerializer
    permission_classes = [AllowAny()]

    def get_queryset(self):
        return Answer.objects.filter(question=self.kwargs['questions_pk'])
