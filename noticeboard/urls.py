from django.urls import path
from .views import (
    NoticeListView,
    NoticeDetailView,
    NoticeUpvoteView,
    NoticeCreateView,
    NoticeDownvoteView,
)

urlpatterns = [
    path("noticeboard/", NoticeListView.as_view()),
    path("noticeboard/create/", NoticeCreateView.as_view()),
    path("noticeboard/<int:pk>/", NoticeDetailView.as_view()),
    path("noticeboard/<int:pk>/upvote/", NoticeUpvoteView.as_view()),
    path("noticeboard/<int:pk>/downvote/", NoticeDownvoteView.as_view()),
]
