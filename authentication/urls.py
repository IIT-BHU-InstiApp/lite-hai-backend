from django.urls import path
from .views import LoginView, ProfileView, ProfileSearchView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/search/", ProfileSearchView.as_view(), name="profile-search"),
]
