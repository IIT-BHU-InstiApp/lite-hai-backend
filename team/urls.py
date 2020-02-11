from django.urls import path
from .views import TeamView

urlpatterns = [
    path('team/', TeamView.as_view(), name='team')
]
