from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_description="회원가입을 처리합니다.")
    def post(self, request, *args, **kwargs):
        """
        회원가입을 처리합니다.

        회원가입을 위한 사용자 데이터를 수신하고 새 사용자를 생성합니다.
        """
        return super().post(request, *args, **kwargs)

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_description="JWT 토큰을 발급합니다.")
    def post(self, request, *args, **kwargs):
        """
        JWT 토큰을 발급합니다.

        사용자 인증 정보를 수신하고 유효한 경우 JWT 토큰을 반환합니다.
        """
        return super().post(request, *args, **kwargs)

class MyTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_description="JWT 토큰을 갱신합니다.")
    def post(self, request, *args, **kwargs):
        """
        JWT 토큰을 갱신합니다.

        리프레시 토큰을 수신하고 유효한 경우 새로운 액세스 토큰을 반환합니다.
        """
        return super().post(request, *args, **kwargs)


