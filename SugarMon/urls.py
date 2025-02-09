"""
URL configuration for SugarMon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SugarMon APIs",
        default_version="1",
        description="멋쟁이사자처럼 한국외대 12기 중앙해커톤 SugarMon API 명세 페이지입니다."
    ),
    public = True,
    permission_classes=(permissions.AllowAny, )
)

urlpatterns = [
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('ateFood/', include('food.urls')),
    path('gIndex/', include('gIndex.urls')),
    path('accounts/', include('allauth.urls')),
    path('checklist/', include('checkList.urls')),
    path('chat/', include('chat.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

ASGI_APPLICATION = 'projectname.routing.application'