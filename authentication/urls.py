from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
]