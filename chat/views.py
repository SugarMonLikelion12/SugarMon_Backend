from .models import User
from .serializers import *
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

class CreateChatRoomAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['채팅'],
            operation_summary="채팅방 만들기",
            operation_description="두 유저가 대화할 수 있는 채팅방을 생성한다.\n(두 유저는 자신들이 속해있는 채팅방의 id를 통해 채팅할 수 있음)",
            request_body=getOpponentSerializer,
            responses={201: openapi.Response(
                description="채팅방 생성 성공",
                schema=createChatRoomSerializer
            ),
            400: "자신과 상대방이 속해있는 채팅방이 이미 존재할 경우"
            })
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        user = request.user
        opponent = User.objects.get(pk=request.data.get('opponentId'))

        isExist = ChatRoom.objects.filter(Q(user1=user, user2=opponent) | Q(user1=opponent, user2=user)).exists()
        if isExist:
            return Response({"message": "이미 해당 두 유저가 포함된 채팅방이 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = createChatRoomSerializer(data={'user1':user.id, 'user2':opponent.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class GetMyChatRoomAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['채팅'],
            operation_summary="내가 속한 채팅방 가져오기",
            operation_description="현재 접속자가 소속되어 있는 채팅방의 id들을 모두 가져온다",
            responses={200: openapi.Response(
                description="불러오기 성공",
                schema=getMyChatRoomSerializer(many=True)
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request):
        user = request.user

        chatRoomList = ChatRoom.objects.filter(Q(user1 = user) | Q(user2 = user))
        serializer = getMyChatRoomSerializer(instance=chatRoomList, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetChatMessagesAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['채팅'],
            operation_summary="채팅방 메세지 불러오기",
            operation_description="특정 채팅방에 접속할 때, 이전의 메세지들을 불러올 때 사용.",
            responses={200: openapi.Response(
                description="불러오기 성공",
                schema=getMessagesSerializer(many=True)
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request, chatRoomId):
        chatRoom = ChatRoom.objects.get(pk=chatRoomId)
        messageList = Message.objects.filter(chatRoom=chatRoom, many=True).order_by('createdAt')

        serializer = getMessagesSerializer(instance=messageList, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)