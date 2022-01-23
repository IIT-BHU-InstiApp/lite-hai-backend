from django.urls import path
from .views import (
    HostelListView, MessListView,
    MessDetailView, MessBillView, MessCancelView
)

urlpatterns = [
    path('hostels/', HostelListView.as_view(), name='hostel-list'),
    path('hostel/<int:pk>/', MessListView.as_view(), name='mess-list'),
    path('mess/<int:pk>/', MessDetailView.as_view(), name='mess-detail'),
    path('mess/<int:pk>/bill/', MessBillView.as_view(), name='bill-detail'),
    path('mess/<int:pk>/cancel/', MessCancelView.as_view(), name='cancel-mess'),
]
