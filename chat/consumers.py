from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
import json

class ChatConsumer(AsyncWebsocketConsumer):
    # 웹소켓 연결 수립 시 실행되는 코드
    async def connect(self):
        try:
            self.chatRoomId = self.scope['url_route']['kwargs']['chatRoomId'] # ChatRoom 객체의 id를 가져온다.

            isRoomExist = await ChatRoom.objects.get(pk=self.chatRoomId) # 해당 id를 가진 방이 존재하는지 확인
            if not isRoomExist:
                raise ValueError("존재하지 않는 채팅방 id입니다.")
            
            groupName = f"chatRoom{self.chatRoomId}" # unique한 그룹 이름
            await self.channel_layer.group_add(groupName, self.channel_name) # 현재 채널을 그룹에 추가
            await self.accept()
            print("웹소켓에 클라이어늩가 연결됨")

        except ValueError as error: # 오류가 있는 경우, 오류 메시지를 반환
            await self.send_json({"error": str(error)})
            await self.close()


    async def disconnect(self, close_code):
        # 웹소켓 연결 해제 시 실행되는 코드
        groupName = f"chatRoom{self.chatRoomId}"
        await self.channel_layer.discard(groupName, self.channel_name) # 현재 채널을 그룹에서 제거


    # 이건 별도의 컨슈머로 만들어야 할 거 같은데?? 메세지 보내고 받는 컨슈머
    async def receive_json(self, data):
        try:
            content = data['content'] # 채팅 내용
            sender = data['user'] # 누가 그 채팅을 보냈는지
            chatRoomId = data['chatRoomId'] # 채팅방 id
            groupName = f"chatRoom{chatRoomId}"

            chatRoom = await ChatRoom.objects.get(pk=chatRoomId)
            if chatRoom.DoesNotExist():
                raise ValueError("존재하지 않는 채팅방 id입니다.")
            
            # 메세지를 DB에 저장
            await self.saveMessage(chatRoom, sender, content)

            # 메세지를 전체 그룹에 전송
            await self.channel_layer.group_send(groupName, {
                "type": "chatMessage",
                "content": content,
                "sender": sender, # 이렇게 하면 센더 객체 전체를 보내게 돼서 리팩토링 필요,
                "chatRoomId": chatRoomId
            })
        
        except ValueError as error:
            await self.send_json({"error": str(error)})

    async def chatMessage(self, event): # 이게 type인가??? // 그룹 내의 다른 클라이언트로부터 메세지를 받아을 때, 그 메세지를 현재 채널(클라이언트)에 전송
        try:
            content = event['content']
            sender = event['sender']
            chatRoomId = event['chatRoomId']
            await self.send_json({"content": content, "sender": sender, "chatRoomId": chatRoomId})

        except Exception as exception:
            await self.send_json({"error": str(exception)})

    @database_sync_to_async # 기본적으로 DB 연산은 동기적이라서, 비동기로 바꿈으로써 웹소켓 비동기 흐름 성능을 개선
    def saveMessage(self, chatRoom, sender, content):
        if not sender or not content:
            raise ValueError("발신자 및 메시지 내용이 필요합니다.")
        
        # 메시지 객체 생성 후 DB에 저장
        Message.objects.create(chatRoom=chatRoom, sender=sender, content=content)