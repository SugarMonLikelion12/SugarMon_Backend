from rest_framework import serializers
from .models import gIndex

class RegisterGISerializer(serializers.ModelSerializer):
    class Meta:
        model = gIndex
        fields = ['id', 'foodName', 'gIndex']

class GetOneGISerializer(serializers.ModelSerializer):
    class Meta:
        model = gIndex
        fields = ['gIndex', 'user']

class GetFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = gIndex
        fields = ['id', 'foodName']