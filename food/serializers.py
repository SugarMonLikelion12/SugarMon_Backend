from rest_framework import serializers
from .models import AteFood

class RegisterAteFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = AteFood
        fields = ['id', 'name', 'ateDate', 'when']

class ResponseAteFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = AteFood
        fields = ['id', 'name', 'ateDate', 'when']