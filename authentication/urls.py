from django.urls import path
from django.conf.urls import url, include
from .views import LoginView, ProfileView, ProfileSearchView
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/search/', ProfileSearchView.as_view(), name='profile-search'),
    url(r'^', include(router.urls)),
  
]
