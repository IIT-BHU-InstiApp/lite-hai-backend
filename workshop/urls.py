from django.urls import path
from .views import (
    CouncilView, CouncilDetailView, ClubDetailView, ClubDetailWorkshopView,
    ClubSubscriptionToggleView, TagCreateView, TagSearchView, WorkshopTagsUpdateView,
    WorkshopActiveAndPastView, WorkshopPastView, WorkshopCreateView, WorkshopDetailView,
    WorkshopActiveView, WorkshopContactsUpdateView, WorkshopInterestedToggleView,
    WorkshopInterestedView, WorkshopSearchView, WorkshopDateSearchView)

urlpatterns = [
    path('councils/', CouncilView.as_view(), name='councils'),
    path('councils/<int:pk>/', CouncilDetailView.as_view(), name='council-detail'),
    path('clubs/<int:pk>/', ClubDetailView.as_view(), name='club-detail'),
    path('clubs/<int:pk>/workshops/', ClubDetailWorkshopView.as_view(), name='club-workshops'),
    path(
        'clubs/<int:pk>/toggle-subscribed/', ClubSubscriptionToggleView.as_view(),
        name='club-togglesubscribed'),
    path('tags/create/', TagCreateView.as_view(), name='tag-create'),
    path('tags/search/', TagSearchView.as_view(), name='tag-search'),
    path('workshops/', WorkshopActiveAndPastView.as_view(), name='workshops'),
    path('workshops/active/', WorkshopActiveView.as_view(), name='active-workshops'),
    path('workshops/past/', WorkshopPastView.as_view(), name='past-workshops'),
    path('workshops/create/', WorkshopCreateView.as_view(), name='create-workshops'),
    path('workshops/<int:pk>/', WorkshopDetailView.as_view(), name='workshop-detail'),
    path(
        'workshops/<int:pk>/update-tags/', WorkshopTagsUpdateView.as_view(),
        name='workshop-update-tags'),
    path(
        'workshops/<int:pk>/update-contacts/', WorkshopContactsUpdateView.as_view(),
        name='workshop-update-contacts'),
    path(
        'workshops/<int:pk>/toggle-interested/', WorkshopInterestedToggleView.as_view(),
        name='workshop-toggle-intrested'),
    path('workshops/interested/', WorkshopInterestedView.as_view(), name='intrested-workshops'),
    path('workshops/search/', WorkshopSearchView.as_view(), name='search-workshops'),
    path('workshops/search/date/', WorkshopDateSearchView.as_view(), name='search-workshops-date'),
]
