from allauth.account.forms import SignupForm, LoginForm
from django import forms

class CustomSignupForm(SignupForm):
    email = forms.EmailField(required=False)  # 이메일 필드를 선택 사항으로 변경
    username = forms.CharField(max_length=100, label='사용자 이름')
    nickname = forms.CharField(max_length=100, label='닉네임')
    isDoctor = forms.BooleanField(required=False, label='의사 여부')

    def signup(self, request, user):
        user.nickname = self.cleaned_data['nickname']
        user.isDoctor = self.cleaned_data['isDoctor']
        user.save()
        return user

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'] = forms.CharField(label='사용자 이름 또는 이메일 주소')

