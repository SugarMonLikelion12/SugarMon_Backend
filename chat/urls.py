from django.urls import path
from .views import *


urlpatterns = [
    path('createChatRoom', CreateChatRoomAPI.as_view()),
    path('getMyChatRoom', GetMyChatRoomAPI.as_view()),
    path('getChatMessages/<int:chatRoomId>', GetChatMessagesAPI.as_view())

    path('rooms/', views.ChatRoomListCreateView.as_view(), name='chat_rooms'),
    path('<int:room_id>/messages', views.MessageListView.as_view(), name='chat_messages'),
]