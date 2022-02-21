from django.urls import path
from .views import (
    CreateLostAndFoundView, LostAndFoundListView)

urlpatterns = [
    path('lostandfound/create/', CreateLostAndFoundView.as_view(),
         name='create_grievance'),
    path('lostandfound/list/',
         LostAndFoundListView.as_view(), name='list_lost_and_found'),
]
