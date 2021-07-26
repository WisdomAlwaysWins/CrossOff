from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from .models import *


class LoginForm(AuthenticationForm):
    username = UsernameField(label=False,
                             widget=forms.TextInput(
                                 attrs={
                                     'autofocus': True,
                                     'placeholder': 'ID를 입력하세요',
                                     'class': 'login_input_id'
                                 }))
    password = forms.CharField(
        strip=False,
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': '비밀번호를 입력하세요',
                'class': 'login_input_pwd'
            }),
    )


class RegisterForm(UserCreationForm):
    username = UsernameField(label='ID',
                             widget=forms.TextInput(
                                 attrs={
                                     'autofocus': True,
                                     'placeholder': 'ID를 입력하세요',
                                     'class': 'register_input_id'
                                 }))
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={
            'placeholder': '비밀번호를 입력하세요',
            'class': 'register_input_password'
        }))
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={
            'placeholder': '동일한 비밀번호를 입력하세요',
            'class': 'register_input_password'
        }))
    nickname = forms.CharField(label='별명', widget=forms.TextInput())
    birthdate = forms.DateField(label='생년월일', widget=forms.SelectDateWidget())
    gender = forms.ChoiceField(label='성별', choices=User.GENDER_CHOICES)
    job = forms.ChoiceField(label='직업', choices=User.JOB_CHOICES)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'username', 'password1', 'password2', 'nickname', 'birthdate',
            'gender', 'job'
        ]
