from django.urls import path
from django.conf.urls import url, include
from .views import LoginView, ProfileView, ProfileSearchView,NotificationView
from fcm_django.api.rest_framework import FCMDeviceViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'devices', FCMDeviceViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/search/', ProfileSearchView.as_view(), name='profile-search'),
    url(r'^', include(router.urls)),
    path('notification/', NotificationView.as_view()),
  
]
