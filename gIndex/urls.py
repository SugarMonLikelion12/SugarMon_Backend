from django.urls import include, path
from .views import *
from . import views

app_name = 'gIndex'

urlpatterns = [
    path('registerGI', registerGIAPI.as_view()),
    path('getGI/<str:foodName>', getGIAPI.as_view()),
]
