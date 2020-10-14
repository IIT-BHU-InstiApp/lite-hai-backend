from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from .views import LoginView, ProfileView, ProfileSearchView


router = DefaultRouter()
router.register(r'devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/search/', ProfileSearchView.as_view(), name='profile-search'),
    path('', include(router.urls)),
]
