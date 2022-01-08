from django.urls import path
from .views import (
    ParliamentContactListView,
    ParliamentContactCreateView,
    ParliamentContactDetailView,
    ParliamentUpdateListView,
    ParliamentUpdateCreateView,
    ParliamentUpdateDetailView,
    ParliamentSuggestionsListView,
    ParliamentSuggestionsCreateView,
    ParliamentSuggestionUpvoteView,
    ParliamentSuggestionDownvoteView,
    ParliamentSuggestionDetailView,
)

urlpatterns = [
    path("parliamentContact/", ParliamentContactListView.as_view()),
    path("parliamentContact/create/", ParliamentContactCreateView.as_view()),
    path("parliamentContact/<int:pk>/", ParliamentContactDetailView.as_view()),
    path("parliamentUpdate/", ParliamentUpdateListView.as_view()),
    path("parliamentUpdate/create/", ParliamentUpdateCreateView.as_view()),
    path("parliamentUpdate/<int:pk>/", ParliamentUpdateDetailView.as_view()),
    path("parliamentSuggestions/", ParliamentSuggestionsListView.as_view()),
    path("parliamentSuggestions/create/", ParliamentSuggestionsCreateView.as_view()),
    path("parliamentSuggestions/<int:pk>/", ParliamentSuggestionDetailView.as_view()),
    path("parliamentSuggestions/<int:pk>/upvote/", ParliamentSuggestionUpvoteView.as_view()),
    path("parliamentSuggestions/<int:pk>/downvote/", ParliamentSuggestionDownvoteView.as_view()),
]
