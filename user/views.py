from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from .models import User
from dj_rest_auth.registration.views import RegisterView
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from django.utils.decorators import method_decorator

class CustomRegisterView(RegisterView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
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

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class GetDoctorUserView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            operation_summary="의사 유저 가져오기",
            operation_description="의사(isDoctor=True)인 유저만 가져온다",
            responses={200: openapi.Response(
                description="불러오기 성공",
                schema=GetDoctorUserSerializer
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request):
        doctorList = User.objects.filter(isDoctor=True)

        serializer = GetDoctorUserSerializer(instance=doctorList, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)