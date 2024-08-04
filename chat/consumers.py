from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import ChatRoom, Message, User
import json

class ChatConsumer(AsyncWebsocketConsumer):
    authentication_classes = [JWTAuthentication]

    # 웹소켓 연결 수립 시 실행되는 코드
    async def connect(self):
        try:
            self.chatRoomId = self.scope['url_route']['kwargs']['chatRoomId'] # ChatRoom 객체의 id를 가져온다.

            isRoomExist = await database_sync_to_async(ChatRoom.objects.get)(pk=self.chatRoomId) # 해당 id를 가진 방이 존재하는지 확인
            if not isRoomExist:
                raise ValueError("존재하지 않는 채팅방 id입니다.")
            
            groupName = f"chatRoom{self.chatRoomId}" # unique한 그룹 이름
            await self.channel_layer.group_add(groupName, self.channel_name) # 현재 채널을 그룹에 추가
            await self.accept()
            print("웹소켓에 클라이어늩가 연결됨")

        except ValueError as error: # 오류가 있는 경우, 오류 메시지를 반환
            await self.send(text_data=json.dumps({"error": str(error)}, ensure_ascii=False)) # send() 함수는 문자열을 받아야 하므로, json.dumps()를 통해 딕셔너리를 문자열으로 덤핑
            await self.close()


    async def disconnect(self, close_code):
        # 웹소켓 연결 해제 시 실행되는 코드
        groupName = f"chatRoom{self.chatRoomId}"
        await self.channel_layer.group_discard(groupName, self.channel_name) # 현재 채널을 그룹에서 제거
        print("웹소켓에 클라이어늩가 연결 해제됨")

    # 메세지 받았을 때 실행되는 함수
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # 발송자 정보 가져오기
        rawToken = data['authorization']
        try:
            accessToken = AccessToken(rawToken[7:])
            senderId = accessToken.payload['user_id']
            sender = await database_sync_to_async(User.objects.get)(pk=senderId)
        except jwt.ExpiredSignatureError:
            raise ValueError(f"만료된 토큰입니다.: {rawToken}")
        except jwt.InvalidTokenError:
            raise ValueError(f"잘못된 토큰입니다.: {rawToken}")

        try:
            content = data['content'] # 채팅 내용
            chatRoomId = data['chatRoomId'] # 채팅방 id
            groupName = f"chatRoom{chatRoomId}"

            try:
                chatRoom = await database_sync_to_async(ChatRoom.objects.get)(pk=chatRoomId)
            except ObjectDoesNotExist:
                raise ValueError(f"존재하지 않는 채팅방 id입니다: {chatRoomId}")

            # 메세지를 DB에 저장
            await self.saveMessage(chatRoom, sender, content)

            # 메세지를 전체 그룹에 전송
            await self.channel_layer.group_send(groupName, {
                "type": "chatMessage",
                "content": content,
                "senderId": senderId,
                "chatRoomId": chatRoomId
            })
        
        except ValueError as error:
            await self.send(text_data=json.dumps({"error": str(error)}, ensure_ascii=False))

    async def chatMessage(self, event): # 이게 type인가??? // 그룹 내의 다른 클라이언트로부터 메세지를 받아을 때, 그 메세지를 현재 채널(클라이언트)에 전송
        try:
            content = event['content']
            senderId = event['senderId']
            chatRoomId = event['chatRoomId']
            await self.send(text_data=json.dumps({"content": content, "senderId": senderId, "chatRoomId": chatRoomId}, ensure_ascii=False))

        except Exception as exception:
            await self.send(text_data=json.dumps({"error": str(exception)}, ensure_ascii=False))

    @database_sync_to_async # 기본적으로 DB 연산은 동기적이라서, 비동기로 바꿈으로써 웹소켓 비동기 흐름 성능을 개선
    def saveMessage(self, chatRoom, sender, content):
        if not sender or not content:
            raise ValueError("발신자 및 메시지 내용이 필요합니다.")
        
        # 메시지 객체 생성 후 DB에 저장
        Message.objects.create(chatRoom=chatRoom, sender=sender, content=content)