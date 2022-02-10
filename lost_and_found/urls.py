from django.urls import path
from .views import (
    CreateLostAndFoundView, CountLostAndFoundView, LostAndFoundDetailView)

urlpatterns = [
    path('lostandfound/create/', CreateLostAndFoundView.as_view(),
         name='create_grievance'),
    path('lostandfound/count/', CountLostAndFoundView.as_view(),
         name='count_lost_and_found'),
    path('lostandfound/details/<int:st>',
         LostAndFoundDetailView.as_view(), name='detail_lost_and_found'),
]
