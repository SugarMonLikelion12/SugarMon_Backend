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
from rest_framework.views import APIView

# Create your views here.
class registerGIAPI(APIView):
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class getGIAPI(APIView):
    @swagger_auto_schema(
            tags=['혈당지수'],
            operation_summary="혈당지수 가져오기",
            operation_description="음식 이름을 입력하면, 해당 음식의 혈당지수를 가져온다.\n(다른 사람이 등록한 음식의 혈당지수는 가져오지 않고, 기존에 입력되어있던 음식 + 내가 등록한 음식의 혈당지수만 가져옴)",
            #request_body=RegisterGISerializer, -> GET요청에서 받는 파라미터는 이거 명시 안 해줘도 자동으로 처리된다
            responses={
                200: openapi.Response(description="불러오기 성공", schema=GetOneGISerializer),
                400: "해당 음식의 혈당지수 데이터가 존재하지 않는 경우"
            })
    @method_decorator(permission_classes([IsAuthenticated]))
    def get(self, request, foodName):
        user = request.user
        gIndexes = gIndex.objects.filter(Q(user=None) | Q(user=user)) # Q객체를 사용하면, and나 or조건을 사용해서 모델 객체를 가져올 수 있음

        try:
            gi = gIndexes.get(foodName=foodName)
        except gIndex.DoesNotExist: # 해당 음식의 GI지수가 등록 되어있지 않을 때
            return Response({"message": "해당 음식의 혈당지수 데이터가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = GetOneGISerializer(instance=gi)
        return Response(serializer.data, status=status.HTTP_200_OK)