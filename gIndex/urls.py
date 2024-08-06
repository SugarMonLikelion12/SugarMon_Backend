from django.urls import include, path
from .views import *

app_name = 'gIndex'

urlpatterns = [
    path('registerGI', registerGIAPI.as_view()),
    path('getGI/<str:foodName>', getGIAPI.as_view()),
    path('getFood', getFoodAPI.as_view()),
    path('getTodayGI/<int:year>/<int:month>/<int:day>/<int:when>', getTodayGIAPI.as_view()),
]
