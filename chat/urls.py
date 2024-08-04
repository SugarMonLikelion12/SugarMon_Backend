from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('createChatRoom', CreateChatRoomAPI.as_view()),
    path('getMyChatRoom', GetMyChatRoomAPI.as_view()),
    path('getChatMessages/<int:chatRoomId>', GetChatMessagesAPI.as_view()),
    path('checkIfMyMessage', CheckIfMyMessageAPI.as_view()),
]