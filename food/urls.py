from django.urls import include, path
from .views import *
from . import views

app_name = 'ateFood'

urlpatterns = [
    path('registerAteFood', registerAteFoodAPI.as_view()),
    path('getAllAteFoodUser', getAllAteFoodUserAPI.as_view()),
    path('getMonthAteFoodUser/<int:year>/<int:month>', getMonthAteFoodUserAPI.as_view()),
    path('deleteAteFood/<int:ateFoodId>', deleteAteFoodAPI.as_view()),
]
