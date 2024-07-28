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

# Create your views here.
class registerAteFoodAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['먹은음식'],
            operation_summary="먹은음식 등록",
            operation_description="먹은음식 객체를 DB에 저장한다. 리스트에 담아서 여러 개 한번에 여러 개 요청 가능\n\nateDate - 음식을 먹은 날짜를 입력. (입력하지 않을 시 자동으로 오늘 날짜로 등록)\nwhen - 0: 아침, 1: 점심, 2: 저녁, 3: 간식",
            request_body=RegisterAteFoodSerializer(many=True),
            responses={201: openapi.Response(
                description="저장 성공",
                schema=RegisterAteFoodSerializer
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        serializer = RegisterAteFoodSerializer(data=request.data, many=True)
        
        if (serializer.is_valid()):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class getAllAteFoodUserAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['먹은음식'],
            operation_summary="현재 유저가 먹은음식 불러오기",
            operation_description="현재 접속한 유저가 등록한 모든 먹은 음식을 불러온다.",
            responses={200: openapi.Response(
                description="불러오기 성공",
                schema=ResponseAteFoodSerializer(many=True)
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request):
        ateFoodList = AteFood.objects.filter(user=request.user)

        try:
            serializer = ResponseAteFoodSerializer(instance=ateFoodList, many=True)
        except:
            return Response({"message": "직렬화 도중 오류가 발생하였습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class getMonthAteFoodUserAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['먹은음식'],
            operation_summary="특정 년월에 현재 유저가 먹은음식 불러오기",
            operation_description="요청한 year과 month에 현재 접속한 유저가 먹은 음식들을 불러온다.",
            responses={200: openapi.Response(
                description="불러오기 성공",
                schema=ResponseAteFoodSerializer(many=True)
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request, year, month):
        ateFoodList = AteFood.objects.filter(user=request.user, ateDate__year=year, ateDate__month=month)

        try:
            serializer = ResponseAteFoodSerializer(instance=ateFoodList, many=True)
        except:
            return Response({"message": "직렬화 도중 오류가 발생하였습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class deleteAteFoodAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['먹은음식'],
            operation_summary="먹은 음식 삭제하기",
            operation_description="요청한 id의 먹은 음식 데이터를 삭제한다.",
            responses={
                204: openapi.Response(description="삭제 성공"),
                400: openapi.Response(description="잘못된 먹은 음식 id로 요청할 경우")
            })
    @method_decorator(permission_classes([IsAuthenticated]))
    def delete(self, request, ateFoodId):
        try:
            ateFood = AteFood.objects.get(pk=ateFoodId)
        except AteFood.DoesNotExist:
            return Response({"message": "잘못된 먹은 음식 id입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        ateFood.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)