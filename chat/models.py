from django.db import models
from user.models import User
from django.utils import timezone

class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name = "chatRoomAsUser1")
    user2 = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="chatRoomAsUser2")

class Message(models.Model):
    chatRoom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)