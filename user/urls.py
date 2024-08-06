from django.urls import include, path
from .views import *
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserDetailView.as_view(), name='user_detail'),
    path('getDoctorUser/', GetDoctorUserView.as_view()),
]
