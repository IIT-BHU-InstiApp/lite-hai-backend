from django.urls import path
from .views import NoticeGetView, NoticeUpdateView, NoticeVoteView, NoticeCreateView

urlpatterns = [
    path("/", NoticeGetView.as_view()),
    path("/create/", NoticeCreateView.as_view()),
    path("/<int:pk>/", NoticeUpdateView.as_view()),
    path("/<int:pk>/vote/", NoticeVoteView.as_view()),
]
