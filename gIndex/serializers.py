from rest_framework import serializers
from .models import gIndex

class registerGISerializer(serializers.ModelSerializer):
    class Meta:
        model = gIndex
        fields = ['foodName', 'gIndex']