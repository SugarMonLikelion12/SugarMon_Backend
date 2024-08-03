from rest_framework import serializers
from .models import Checklist

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = [
            'id',
            'date',
            'when',
            'meal_order',
            'sugar',
            'exercise',
        ]
        extra_kwargs = {
            'meal_order': {'label': '식사 순서'},
            'sugar': {'label': '식후 액상과당 섭취'},
            'exercise': {'label': '운동 여부'},
        }
