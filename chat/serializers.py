from rest_framework import serializers
from .models import ChatRoom, Message
from user.serializers import getUserSerializer

class getOpponentSerializer(serializers.Serializer):
    opponentId = serializers.IntegerField()

class responseChatRoomSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class createChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'user1', 'user2']

class getMyChatRoomSerializer(serializers.ModelSerializer):
    opponentId = serializers.SerializerMethodField()
    opponentNickname = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'opponentId', 'opponentNickname']

    def get_opponentId(self, obj):
        request = self.context.get('request')
        user = request.user
        return obj.user2.id if obj.user1 == user else obj.user1.id
    
    def get_opponentNickname(self, obj):
        request = self.context.get('request')
        user = request.user
        return obj.user2.nickname if obj.user1 == user else obj.user1.nickname

class getMessagesSerializer(serializers.ModelSerializer):
    isMyChat = serializers.SerializerMethodField() # 해당 메시지가 현재 접속자가 보낸 채팅이라면 True, 아니면 False

    class Meta:
        model = Message
        fields = ['sender', 'content', 'createdAt', 'isMyChat']
    
    def get_isMyChat(self, obj):
        request = self.context.get('request')
        user = request.user
        return obj.sender == user

# Message 모델에 대한 시리얼라이저 클래스입니다.
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message  # Message 모델을 기반으로 합니다.
        fields = "__all__"  # 모든 필드를 포함시킵니다.

# ChatRoom 모델에 대한 시리얼라이저 클래스입니다.
class ChatRoomSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()  # 최신 메시지 필드를 동적으로 가져옵니다.
    opponent_email = serializers.SerializerMethodField()  # 상대방 이메일 필드를 동적으로 가져옵니다.
    shop_user_email = serializers.SerializerMethodField()  # 상점 사용자의 이메일을 가져오는 필드입니다.
    visitor_user_email = serializers.SerializerMethodField()  # 방문자 사용자의 이메일을 가져오는 필드입니다.
    messages = MessageSerializer(many=True, read_only=True, source="messages.all")  # 해당 채팅방의 메시지 목록을 가져옵니다.

    class Meta:
        model = ChatRoom  # ChatRoom 모델을 기반으로 합니다.
        # 시리얼라이즈할 필드들을 지정합니다.
        fields = ('id', 'shop_user_email', 'visitor_user_email', 'latest_message', 'opponent_email', 'messages')

    # 최신 메시지를 가져오는 메소드입니다.
    def get_latest_message(self, obj):
        latest_msg = Message.objects.filter(room=obj).order_by('-timestamp').first()  # 최신 메시지를 조회합니다.
        if latest_msg:
            return latest_msg.text  # 최신 메시지의 내용을 반환합니다.
        return None  # 메시지가 없다면 None을 반환합니다.

    # 요청 사용자와 대화하는 상대방의 이메일을 가져오는 메소드입니다.
    def get_opponent_email(self, obj):
        request_user_email = self.context['request'].query_params.get('email', None)
        # 요청한 사용자가 상점 사용자일 경우, 방문자의 이메일을 반환합니다.
        if request_user_email == obj.shop_user.shop_user_email:
            return obj.visitor_user.visitor_user_email
        else:  # 그렇지 않다면, 상점 사용자의 이메일을 반환합니다.
            return obj.shop_user.shop_user_email

    # shop_user의 이메일을 반환하는 메소드입니다.
    def get_shop_user_email(self, obj):  
        return obj.shop_user.shop_user_email

    # visitor_user의 이메일을 반환하는 메소드입니다.
    def get_visitor_user_email(self, obj):  
        return obj.visitor_user.visitor_user_email
    
class GetMessageSenderIdSerializer(serializers.Serializer):
    senderId = serializers.IntegerField()

class CheckIfMyMessageSerializer(serializers.Serializer):
    isMe = serializers.BooleanField()