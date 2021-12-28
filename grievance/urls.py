from django.urls import path
from .views import (
    CreateGrievanceView, CountGrievanceView, GrievanceDetailView)

urlpatterns = [
    path('grievance/create/', CreateGrievanceView.as_view(),
         name='create_grievance'),
    path('grievance/count/', CountGrievanceView.as_view(), name='count_grievance'),
    path('grievance/details/<int:st>',
         GrievanceDetailView.as_view(), name='detail_grievance'),
]
