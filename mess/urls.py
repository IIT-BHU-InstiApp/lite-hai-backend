from django.urls import path
from .views import (
    HostelListView, MessListView,
    MessDetailView, MessBillView
)

urlpatterns = [
    path('hostel/', HostelListView.as_view(), name='hostel-list'),
    path('hostel/<int:pk>/', MessListView.as_view(), name='mess-list'),
    path('mess/<int:pk>/', MessDetailView.as_view(), name='mess-detail'),
    path('mess/<int:pk>/bill/<int:month>/',
         MessBillView.as_view(), name='bill-detail'),
]
