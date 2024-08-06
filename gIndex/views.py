from .serializers import *
from food.models import AteFood
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
class registerGIAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['혈당지수'],
            operation_summary="혈당지수 등록",
            operation_description="혈당지수(gIndex) 객체를 DB에 저장한다.",
            request_body=RegisterGISerializer,
            responses={201: openapi.Response(
                description="저장 성공",
                schema=RegisterGISerializer
            )})
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        serializer = RegisterGISerializer(data=request.data)

        if (serializer.is_valid()):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class getGIAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['혈당지수'],
            operation_summary="혈당지수 가져오기",
            operation_description="음식 이름으로 요청하면, 해당 음식의 혈당지수를 가져온다.\n\n(다른 사람이 등록한 혈당지수는 가져오지 않고, 기존에 입력되어있던 혈당지수 + 현재 사용자가 등록한 혈당지수만 가져옴)",
            responses={
                200: openapi.Response(description="불러오기 성공", schema=GetOneGISerializer),
                400: "해당 음식의 혈당지수 데이터가 존재하지 않는 경우"
            })
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request, foodName):
        user = request.user
        
        try:
            gi = gIndex.objects.get(Q(foodName=foodName) & (Q(user=None) | Q(user=user)))
        except gIndex.DoesNotExist: # 해당 음식의 GI지수가 등록 되어있지 않을 때
            return Response({"message": "해당 음식의 혈당지수 데이터가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = GetOneGISerializer(instance=gi)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class getFoodAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['혈당지수'],
            operation_summary="등록된 음식 이름 가져오기",
            operation_description="혈당지수가 등록되어있는 음식들의 이름을 가져온다.\n\n(다른 사람이 등록한 혈당지수의 이름은 가져오지 않고, 기존에 입력되어있던 혈당지수 객체 + 현재 사용자가 등록한 혈당지수 객체의 음식 이름만 가져옴)",
            responses={
                200: openapi.Response(description="불러오기 성공", schema=GetFoodSerializer(many=True)),
                400: "해당 음식의 혈당지수 데이터가 존재하지 않는 경우\n또는 기타 오류"
            })
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request):
        user = request.user

        gindexes = gIndex.objects.filter(Q(user=None) | Q(user=user))
        try:
            serializer = GetFoodSerializer(instance=gindexes, many=True)
        except:
            return Response({"message": "직렬화 도중 오류가 발생하였습니다."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=  status.HTTP_200_OK)

class getTodayGIAPI(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            tags=['혈당지수'],
            operation_summary="해당 날짜 특정 시간대 먹은 음식 gi 총합",
            operation_description="해당 날짜 특정 시간대 먹은 음식 gi 총합 가져옴",
            responses={
                200: openapi.Response(description="불러오기 성공", schema=responseGISerializer),
            })
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request, year, month, day, when):
        user = request.user

        giSum = 0
        ateFoodList = AteFood.objects.filter(user=user, ateDate__year=year, ateDate__month=month, ateDate__day=day, when=when).order_by('ateDate')
        for ateFood in ateFoodList:
            try:
                gi = gIndex.objects.filter(Q(foodName=ateFood.name) & Q(Q(user=user) | Q(user=None))).first()
                giSum += gi.gIndex
            except gIndex.DoesNotExist:
                continue

        serializer = responseGISerializer({'gI': giSum})
        return Response(serializer.data, status=status.HTTP_200_OK)