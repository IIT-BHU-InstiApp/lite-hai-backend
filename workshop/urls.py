from django.urls import path
from .views import (
    ClubTagDeleteView, CouncilView, CouncilDetailView, ClubDetailView, ClubDetailWorkshopView,
    ClubTagsView, ClubSubscriptionToggleView, EntityDetailView, EntityDetailWorkshopView,
    EntityTagCreateView, EntityTagDeleteView, EntityTagSearchView, EntityTagsView, EntityView,
    ClubTagCreateView, ClubTagSearchView, WorkshopTagsUpdateView, EntitySubscriptionToggleView,
    WorkshopActiveAndPastView, WorkshopPastView, ClubWorkshopCreateView, WorkshopDetailView,
    WorkshopActiveView, WorkshopContactsUpdateView, WorkshopInterestedToggleView,
    WorkshopInterestedView, WorkshopSearchView, WorkshopDateSearchView, WorkshopResourceCreateView,
    WorkshopResourceView, EntityWorkshopCreateView, CouncilSubscribeView, CouncilUnsubscribeView)
# from .views import *

urlpatterns = [
    path('councils/', CouncilView.as_view()),
    path('councils/<int:pk>/', CouncilDetailView.as_view()),
    path('councils/<int:pk>/subscribe/', CouncilSubscribeView.as_view()),
    path('councils/<int:pk>/unsubscribe/', CouncilUnsubscribeView.as_view()),

    path('clubs/<int:pk>/', ClubDetailView.as_view()),
    path('clubs/<int:pk>/workshops/', ClubDetailWorkshopView.as_view()),
    path('clubs/<int:pk>/tags/', ClubTagsView.as_view()),
    path('clubs/<int:pk>/tags/create/', ClubTagCreateView.as_view()),
    path('clubs/<int:pk>/tags/delete/', ClubTagDeleteView.as_view()),
    path('clubs/<int:pk>/tags/search/', ClubTagSearchView.as_view()),
    path('clubs/<int:pk>/toggle-subscribed/', ClubSubscriptionToggleView.as_view()),
    path('clubs/<int:pk>/workshops/create/', ClubWorkshopCreateView.as_view()),

    path('workshops/', WorkshopActiveAndPastView.as_view()),
    path('workshops/active/', WorkshopActiveView.as_view()),
    path('workshops/past/', WorkshopPastView.as_view()),
    path('workshops/<int:pk>/', WorkshopDetailView.as_view()),
    path('workshops/<int:pk>/update-tags/', WorkshopTagsUpdateView.as_view()),
    path('workshops/<int:pk>/update-contacts/', WorkshopContactsUpdateView.as_view()),
    path('workshops/<int:pk>/toggle-interested/', WorkshopInterestedToggleView.as_view()),
    path('workshops/<int:pk>/resources/', WorkshopResourceCreateView.as_view()),
    path('workshops/interested/', WorkshopInterestedView.as_view()),
    path('workshops/search/', WorkshopSearchView.as_view()),
    path('workshops/search/date/', WorkshopDateSearchView.as_view()),
    path('resources/<int:pk>/', WorkshopResourceView.as_view()),

    path('entities/', EntityView.as_view()),
    path('entities/<int:pk>/', EntityDetailView.as_view()),
    path('entities/<int:pk>/tags/', EntityTagsView.as_view()),
    path('entities/<int:pk>/tags/create/', EntityTagCreateView.as_view()),
    path('entities/<int:pk>/tags/delete/', EntityTagDeleteView.as_view()),
    path('entities/<int:pk>/tags/search/', EntityTagSearchView.as_view()),
    path('entities/<int:pk>/toggle-subscribed/', EntitySubscriptionToggleView.as_view()),
    path('entities/<int:pk>/workshops/', EntityDetailWorkshopView.as_view()),
    path('entities/<int:pk>/workshops/create/', EntityWorkshopCreateView.as_view()),
]
