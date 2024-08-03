from rest_framework import serializers
from .models import User

class getUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']