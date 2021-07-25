from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from .models import *

class LoginForm(AuthenticationForm):
    username = UsernameField(
        label=False,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder' : 'ID를 입력하세요', 'class' : 'login_input_id'}))
    password = forms.CharField(
        strip=False,
        label=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder' : '비밀번호를 입력하세요', 'class' : 'login_input_pwd'}),
    )

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')