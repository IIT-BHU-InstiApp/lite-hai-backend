from django.urls import path
from .views import NoticeGetView, NoticeUpdateView, NoticeVoteView, NoticeCreateView

urlpatterns = [
    path("noticeboard/", NoticeGetView.as_view()),
    path("noticeboard/create/", NoticeCreateView.as_view()),
    path("noticeboard/<int:pk>/", NoticeUpdateView.as_view()),
    path("noticeboard/<int:pk>/vote/", NoticeVoteView.as_view()),
]
