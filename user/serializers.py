from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)
    isDoctor = serializers.BooleanField(required=False)

    class Meta:
        fields = ('username', 'password1', 'password2', 'nickname', 'isDoctor')

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['isDoctor'] = self.validated_data.get('isDoctor', False)
        return data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.cleaned_data.get('nickname')
        user.isDoctor = self.cleaned_data.get('isDoctor')
        user.save()
        return user

class getUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'isDoctor')


class GetDoctorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']