from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, UserChangeForm, PasswordChangeForm
from django.db.models import fields
from django.http import request
from django.utils import timezone
from .models import *


class LoginForm(AuthenticationForm):
    username = UsernameField(label=False,
                             widget=forms.TextInput(
                                 attrs={
                                     'autofocus': True,
                                     'placeholder': ' ID',
                                     'class': 'login_idForm'
                                 }))
    password = forms.CharField(
        strip=False,
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': ' PW',
                'class': 'login_pwForm'
            }),
    )
    error_messages = {
        'invalid_login': "비밀번호나 ID가 올바르지 않습니다.",
        'inactive': "이 계정은 활성화되지 않았습니다.",
    }


class RegisterForm(UserCreationForm):
    year = timezone.now().year
    years = [x for x in range(1970, year + 1)]
    username = UsernameField(label='ID',
                             widget=forms.TextInput(
                                 attrs={
                                     'autofocus': True,
                                     'placeholder': '',
                                     'class': 'register_idForm'
                                 }))
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={
            'placeholder': '',
            'class': 'register_pwForm'
        }))
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={
            'placeholder': '',
            'class': 'register_pwcheckForm'
        }))
    nickname = forms.CharField(
        label='별명',
        widget=forms.TextInput(attrs={'class': 'register_nicknameForm'}))
    birthdate = forms.DateField(
        label='생년월일',
        widget=forms.SelectDateWidget(years=years, attrs={'class': 'register_birthForm', 'default': 1990}))
    gender = forms.ChoiceField(
        label='성별',
        choices=User.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'register_genderForm'}))
    job = forms.ChoiceField(
        label='직업',
        choices=User.JOB_CHOICES,
        widget=forms.Select(attrs={'class': 'register_jobForm'}))

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


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ['nickname', 'birthdate', 'gender', 'job', ]


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기본 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })
