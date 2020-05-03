from django.urls import path
from .views import (
    CouncilView, CouncilDetailView, ClubDetailView, ClubDetailWorkshopView,
    ClubSubscriptionToggleView, TagCreateView, TagSearchView, WorkshopTagsUpdateView,
    WorkshopActiveAndPastView, WorkshopPastView, WorkshopCreateView, WorkshopDetailView,
    WorkshopActiveView, WorkshopContactsUpdateView, WorkshopInterestedToggleView,
    WorkshopInterestedView, WorkshopSearchView, WorkshopDateSearchView, WorkshopResourceCreateView,
    WorkshopResourceView)

urlpatterns = [
    path('councils/', CouncilView.as_view()),
    path('councils/<int:pk>/', CouncilDetailView.as_view()),
    path('clubs/<int:pk>/', ClubDetailView.as_view()),
    path('clubs/<int:pk>/workshops/', ClubDetailWorkshopView.as_view()),
    path('clubs/<int:pk>/toggle-subscribed/', ClubSubscriptionToggleView.as_view()),
    path('tags/create/', TagCreateView.as_view()),
    path('tags/search/', TagSearchView.as_view()),
    path('workshops/', WorkshopActiveAndPastView.as_view()),
    path('workshops/active/', WorkshopActiveView.as_view()),
    path('workshops/past/', WorkshopPastView.as_view()),
    path('workshops/create/', WorkshopCreateView.as_view()),
    path('workshops/<int:pk>/', WorkshopDetailView.as_view()),
    path('workshops/<int:pk>/update-tags/', WorkshopTagsUpdateView.as_view()),
    path('workshops/<int:pk>/update-contacts/', WorkshopContactsUpdateView.as_view()),
    path('workshops/<int:pk>/toggle-interested/', WorkshopInterestedToggleView.as_view()),
    path('workshops/<int:pk>/resources/', WorkshopResourceCreateView.as_view()),
    path('workshops/interested/', WorkshopInterestedView.as_view()),
    path('workshops/search/', WorkshopSearchView.as_view()),
    path('workshops/search/date/', WorkshopDateSearchView.as_view()),
    path('resources/<int:pk>/', WorkshopResourceView.as_view()),
]
