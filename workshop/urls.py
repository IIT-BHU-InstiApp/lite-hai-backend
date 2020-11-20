from django.urls import path
from .views import (
    CouncilView, CouncilDetailView, ClubDetailView, ClubDetailWorkshopView, ClubTagsView,
    ClubSubscriptionToggleView, EntityDetailView, EntityDetailWorkshopView, EntitySubscriptionToggleView, EntityTagCreateView, EntityTagSearchView, EntityTagsView, EntityWorkshopActiveAndPastView, EntityWorkshopActiveView, EntityWorkshopCreateView, EntityWorkshopDateSearchView, EntityWorkshopInterestedView, EntityWorkshopPastView, EntityWorkshopSearchView, TagCreateView, TagSearchView, WorkshopTagsUpdateView,
    WorkshopActiveAndPastView, WorkshopPastView, WorkshopCreateView, WorkshopDetailView,
    WorkshopActiveView, WorkshopContactsUpdateView, WorkshopInterestedToggleView,
    WorkshopInterestedView, WorkshopSearchView, WorkshopDateSearchView, WorkshopResourceCreateView,
    WorkshopResourceView)

urlpatterns = [
    path('councils/', CouncilView.as_view()),
    path('councils/<int:pk>/', CouncilDetailView.as_view()),
    path('clubs/<int:pk>/', ClubDetailView.as_view()),
    path('clubs/<int:pk>/workshops/', ClubDetailWorkshopView.as_view()),
    path('clubs/<int:pk>/tags/', ClubTagsView.as_view()),
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

    path('entities/<int:pk>/', EntityDetailView.as_view()),
    path('entities/<int:pk>/workshops/', EntityDetailWorkshopView.as_view()),
    path('entities/<int:pk>/tags/', EntityTagsView.as_view()),
    path('entities/<int:pk>/toggle-subscribed/', EntitySubscriptionToggleView.as_view()),

    # Separate end points should not be there
    path('tags/entities/create/', EntityTagCreateView.as_view()),
    path('tags/entities/search/', EntityTagSearchView.as_view()),
    path('workshops/entities/', EntityWorkshopActiveAndPastView.as_view()),
    path('workshops/entities/active/', EntityWorkshopActiveView.as_view()),
    path('workshops/entities/past/', EntityWorkshopPastView.as_view()),
    path('workshops/entities/create/', EntityWorkshopCreateView.as_view()),
    path('workshops/entities/interested/', EntityWorkshopInterestedView.as_view()),
    path('workshops/entities/search/', EntityWorkshopSearchView.as_view()),
    path('workshops/entities/search/date/', EntityWorkshopDateSearchView.as_view()),
]
