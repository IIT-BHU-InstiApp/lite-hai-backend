from django.urls import path
from .views import (
    NoticeGetView,
    NoticeUpdateView,
    NoticeUpvoteView,
    NoticeCreateView,
    NoticeDownvoteView,
)

urlpatterns = [
    path("noticeboard/", NoticeGetView.as_view()),
    path("noticeboard/create/", NoticeCreateView.as_view()),
    path("noticeboard/<int:pk>/", NoticeUpdateView.as_view()),
    path("noticeboard/<int:pk>/upvote/", NoticeUpvoteView.as_view()),
    path("noticeboard/<int:pk>/downvote/", NoticeDownvoteView.as_view()),
]
