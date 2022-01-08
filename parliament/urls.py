from django.urls import path
from .views import (
    ParliamentContactListView,
    ParliamentContactCreateView,
    ParliamentContactDetailView,
    ParliamentUpdateListView,
    ParliamentUpdateCreateView,
    ParliamentUpdateDetailView,
)

urlpatterns = [
    path("parliamentContact/", ParliamentContactListView.as_view()),
    path("parliamentContact/create/", ParliamentContactCreateView.as_view()),
    path("parliamentContact/<int:pk>/", ParliamentContactDetailView.as_view()),
    path("parliamentUpdate/", ParliamentUpdateListView.as_view()),
    path("parliamentUpdate/create/", ParliamentUpdateCreateView.as_view()),
    path("parliamentUpdate/<int:pk>/", ParliamentUpdateDetailView.as_view()),
]
