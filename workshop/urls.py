from django.urls import path
from .views import (
    CouncilView, CouncilDetailView, ClubDetailView, ClubSubscriptionToggleView,
    WorkshopActivePastView, WorkshopPastView, WorkshopCreateView,
    WorkshopDetailView, WorkshopActiveView)

urlpatterns = [
    path('councils/', CouncilView.as_view()),
    path('councils/<int:pk>/', CouncilDetailView.as_view()),
    path('clubs/<int:pk>/', ClubDetailView.as_view()),
    path('clubs/<int:pk>/toggle-subscribed/', ClubSubscriptionToggleView.as_view()),
    path('workshops/', WorkshopActivePastView.as_view()),
    path('workshops/active/', WorkshopActiveView.as_view()),
    path('workshops/past/', WorkshopPastView.as_view()),
    path('workshops/create/', WorkshopCreateView.as_view()),
    path('workshops/<int:pk>/', WorkshopDetailView.as_view()),
]
