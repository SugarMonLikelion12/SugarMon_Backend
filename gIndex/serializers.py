from rest_framework import serializers
from .models import gIndex

class RegisterGISerializer(serializers.ModelSerializer):
    class Meta:
        model = gIndex
        fields = ['foodName', 'gIndex']

class GetOneGISerializer(serializers.ModelSerializer):
    class Meta:
        model = gIndex
        fields = '__all__'