from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Room 모델: 채팅룸을 정의합니다.
class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)

# Message 모델: 채팅 메시지를 정의합니다.
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)  # 메시지가 속한 채팅룸
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # 메시지 발신자
    content = models.TextField()  # 메시지 내용
    timestamp = models.DateTimeField(auto_now_add=True)  # 메시지 작성 일자

