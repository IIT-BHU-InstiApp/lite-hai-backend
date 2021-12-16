"""workshops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

admin.site.site_header = 'IIT BHU Workshops App Backend Administration'

schema_view = get_schema_view(
    openapi.Info(
        title="IIT BHU Workshops App API",
        default_version='v1',
        description=
        """
This is the official IIT BHU Workshops App API developed using Django Rest Framework.

The source code can be found [here](https://github.com/IIT-BHU-InstiApp/lite-hai-backend).
        """,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('authentication.urls')),
    path('', include('config.urls')),
    path('', include('workshop.urls')),
    path('', include('team.urls')),
    path('',include('noticeboard.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
