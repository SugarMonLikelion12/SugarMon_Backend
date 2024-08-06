from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Checklist
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from datetime import date, timedelta
from rest_framework import status

class ChecklistListCreateView(generics.ListCreateAPIView):
    serializer_class = ChecklistSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="체크리스트 항목을 조회하거나 생성합니다.")
    def get_queryset(self):
        return Checklist.objects.filter(user=self.request.user)

    @swagger_auto_schema(operation_description="체크리스트 항목을 생성합니다.")
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChecklistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChecklistSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="특정 체크리스트 항목을 조회, 수정 또는 삭제합니다.")
    def get_queryset(self):
        return Checklist.objects.filter(user=self.request.user)

class DailyChecklistView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="오늘의 체크리스트를 조회합니다.")
    def get(self, request, *args, **kwargs):
        checklist, created = Checklist.objects.get_or_create(
            user=request.user,
            date=date.today()
        )
        serializer = ChecklistSerializer(checklist)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="오늘의 체크리스트를 업데이트합니다.")
    def post(self, request, *args, **kwargs):
        checklist, created = Checklist.objects.get_or_create(
            user=request.user,
            date=date.today()
        )
        serializer = ChecklistSerializer(checklist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class countContinuousChecklist(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="연속 체크리스트 수 조회합니다.")
    def get(self, request):
        user = request.user
        today = date.today()

        count = 0;
        try:
            while (True):
                checklistMorning = Checklist.objects.get(user=user, date=today, when=0)

                if not (checklistMorning.meal_order == True & checklistMorning.sugar == True & checklistMorning.exercise == True):
                    break
            
                checklistNoon = Checklist.objects.get(user=user, date=today, when=1)
                if not (checklistNoon.meal_order == True & checklistNoon.sugar == True & checklistNoon.exercise == True):
                    break
            
                checklistEvening = Checklist.objects.get(user=user, date=today, when=2)
                if not (checklistEvening.meal_order == True & checklistEvening.sugar == True & checklistEvening.exercise == True):
                    break

                count += 1
                today = today - timedelta(days=1)
        except:
            pass

        serializer = responseContinuousChecklist({'days': count})
        return Response(serializer.data, status=status.HTTP_200_OK)

            