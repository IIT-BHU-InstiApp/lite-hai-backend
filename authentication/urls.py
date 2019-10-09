from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
]