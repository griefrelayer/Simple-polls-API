"""
polls_api URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.authtoken import views
from main.viewsets import PollViewSet, QuestionViewSet, AnsweredPollsView, AnsweredPollQuestionView

# API routing
router = routers.DefaultRouter()
router.register(r'polls', PollViewSet, basename="PollView")

# API nested routing
polls_router = routers.NestedDefaultRouter(router, r'polls', lookup="polls")
polls_router.register(r'questions', QuestionViewSet, basename="poll-questions")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(polls_router.urls)),
    path('api/v1/token-auth/', views.obtain_auth_token),
    path('api/v1/users/<int:pk>/polls', AnsweredPollsView.as_view()),
    path('api/v1/users/<int:pk>/polls/<int:pk2>', AnsweredPollQuestionView.as_view()),

]
