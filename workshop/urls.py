from django.urls import path
from .views import (
    CouncilView, CouncilDetailView, ClubDetailView, ClubSubscriptionToggleView,
    ActiveAndPastWorkshopView, PastWorkshopView, WorkshopCreateView, WorkshopDetailView,
    ActiveWorkshopView, WorkshopContactAddView, WorkshopInterestedToggleView,
    WorkshopInterestedView, WorkshopSearchView, WorkshopDateSearchView)

urlpatterns = [
    path('councils/', CouncilView.as_view()),
    path('councils/<int:pk>/', CouncilDetailView.as_view()),
    path('clubs/<int:pk>/', ClubDetailView.as_view()),
    path('clubs/<int:pk>/toggle-subscribed/', ClubSubscriptionToggleView.as_view()),
    path('workshops/', ActiveAndPastWorkshopView.as_view()),
    path('workshops/active/', ActiveWorkshopView.as_view()),
    path('workshops/past/', PastWorkshopView.as_view()),
    path('workshops/create/', WorkshopCreateView.as_view()),
    path('workshops/<int:pk>/', WorkshopDetailView.as_view()),
    path('workshops/<int:pk>/add-contacts/', WorkshopContactAddView.as_view()),
    path('workshops/<int:pk>/toggle-interested/', WorkshopInterestedToggleView.as_view()),
    path('workshops/interested/', WorkshopInterestedView.as_view()),
    path('workshops/search/', WorkshopSearchView.as_view()),
    path('workshops/search/date/', WorkshopDateSearchView.as_view()),
]
