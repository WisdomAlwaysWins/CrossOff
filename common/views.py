from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView
from .forms import *
from .models import *
from mandalart.models import *
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import resolve_url
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib.auth import (
    REDIRECT_FIELD_NAME,
    get_user_model,
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash,
)
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext_lazy as _

User = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.errors:
            return render(request, 'common/register.html', {'form': form})
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('mandalart:new')
    else:
        if request.user.is_authenticated:
            return redirect('mandalart:new')
        form = RegisterForm()
        return render(request, 'common/register.html', {'form': form})


def login_(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.errors:
            return render(request, 'common/login.html', {'form': form})
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request,
                                username=username,
                                password=password)
            if user is not None:
                login(request, user)
                remember_session = request.POST.get('keepLogin', False)
                if remember_session:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                return redirect('mandalart:new')
        else:
            return redirect('home:home')

    else:
        form = LoginForm()
        return render(request, 'common/login.html', {'form': form})


def logout_(request):
    logout(request)
    return redirect('home:home')


@login_required
def dashboard(request, id):
    user = User.objects.get(id=id)
    todos = user.todo.all()
    todolst = {}
    for todo in todos:
        todolst[todo.id] = todo.content
    lst = []
    if not user.is_manda:
        return redirect('mandalart:new')
    manda = Mandalart.objects.get(user=user.id)
    big = BigGoal.objects.get(manda=manda)
    lst.append((big.content, big.is_achieved))
    mid = MidGoal.objects.filter(big=big).order_by('id')
    lst2 = []
    lst4 = {}
    lst5 = {}
    midcnt = 0
    achieve_spe_num = 0
    for i in range(len(mid)):
        specnt = 0
        lst3 = []
        lst6 = []
        lst2.append(mid[i].content)
        spe = SpecificGoal.objects.filter(mid=mid[i]).order_by('id')
        for j in range(len(spe)):
            lst3.append(spe[j].content)
            lst6.append(spe[j].is_achieved)
            if spe[j].is_achieved:
                specnt += 1
                achieve_spe_num += 1
        if specnt == 8:
            mid[i].is_achieved = True
            mid[i].save()
            midcnt += 1
        elif specnt < 8:
            mid[i].is_achieved = False
            mid[i].save()

        lst4[i] = lst3
        lst5[i] = lst6
    if midcnt == 8:
        big.is_achieved = True
        big.save()
    elif midcnt < 8:
        big.is_achieved = False
        big.save()
    achieve_num = achieve_spe_num
    check_mid_achieve = []
    check_big_achieve = []
    if big.is_achieved:
        check_big_achieve.append(1)
    else:
        check_big_achieve.append(0)
    for i in range(len(mid)):
        if mid[i].is_achieved == True:
            # mid goal을 달성했으면 1 저장
            check_mid_achieve.append(1)
        else:
            # 달성하지 못했으면 0 저장
            check_mid_achieve.append(0)
    return render(
        request, 'common/dashboard.html', {
            'user': user,
            'manda': json.dumps(lst, ensure_ascii=False),
            'manda_mid': json.dumps(lst2, ensure_ascii=False),
            'manda_small': json.dumps(lst4, ensure_ascii=False),
            'manda_small_achieve': json.dumps(lst5, ensure_ascii=False),
            'manda_mid1': json.dumps(lst2[0], ensure_ascii=False),
            'manda_mid2': json.dumps(lst2[1], ensure_ascii=False),
            'manda_mid3': json.dumps(lst2[2], ensure_ascii=False),
            'manda_mid4': json.dumps(lst2[3], ensure_ascii=False),
            'manda_mid5': json.dumps(lst2[4], ensure_ascii=False),
            'manda_mid6': json.dumps(lst2[5], ensure_ascii=False),
            'manda_mid7': json.dumps(lst2[6], ensure_ascii=False),
            'manda_mid8': json.dumps(lst2[7], ensure_ascii=False),
            'achieve_num': achieve_num,
            'check_mid_achieve': json.dumps(check_mid_achieve),
            'check_big_achieve': json.dumps(check_big_achieve),
            'todos': json.dumps(todolst, ensure_ascii=False)
        })


@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'common/seeProfile.html', {'user': user})


# def password_reset(request):
#     return render(request, 'common/password_reset.html')

# def password_reset_done(request):
#     return render(request, 'common/password_reset_done.html')

# def password_reset_done_fail(request):
#     return render(request, 'common/password_reset_done_fail.html')

# def password_reset_confirm(request):
#     return render(request, 'common/password_reset_confirm.html')

# def password_reset_complete(request):
#     return render(request, 'common/password_reset_complete.html')


@login_required
def profileUpdate(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST,
                                                instance=request.user)

        if user_change_form.is_valid():
            user_change_form.save()
        return redirect('/common/dashboard/' + str(request.user.id))
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        return render(request, 'common/updateProfile.html',
                      {'user_change_form': user_change_form})


@login_required
def passwordEdit(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(
            request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('/common/dashboard/' + str(request.user.id))
    else:
        password_change_form = CustomPasswordChangeForm(request.user)
    return render(request, 'common/editPassword.html',
                  {'password_change_form': password_change_form})


# class UserPasswordResetView(auth_views.PasswordResetView):
#     template_name = 'password_reset_form.html' #템플릿을 변경하려면 이와같은 형식으로 입력

#     def form_valid(self, form):
#         if User.objects.filter(email=self.request.POST.get("email")).exists():
#             opts = {
#                 'use_https': self.request.is_secure(),
#                 'token_generator': self.token_generator,
#                 'from_email': self.from_email,
#                 'email_template_name': self.email_template_name,
#                 'subject_template_name': self.subject_template_name,
#                 'request': self.request,
#                 'html_email_template_name': self.html_email_template_name,
#                 'extra_email_context': self.extra_email_context,
#             }
#             form.save(**opts)
#             return super().form_valid(form)
#         else:
#             return render(self.request, 'password_reset_done_fail.html')


class UserPasswordResetView(PasswordResetView):
    template_name = 'common/password_reset.html'  # 템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'common/password_reset_done_fail.html')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'common/password_reset_done.html'  # 템플릿을 변경하려면 이와같은 형식으로 입력


class UserPasswordResetConfirmView(PasswordResetConfirmView):

    form_class = CustomPasswordSetForm
    success_url = reverse_lazy('password_reset_complete')

    template_name = 'common/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'common/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


@login_required
def selectionForm(request, id):
    user = User.objects.get(id=id)
    if not user.is_manda:
        return redirect('mandalart:new')

    manda = Mandalart.objects.get(user=user.id)
    big = BigGoal.objects.get(manda=manda)
    mid = MidGoal.objects.filter(big=big).order_by('id')
    lst2 = []
    lst4 = {}
    lst5 = {}
    for i in range(len(mid)):
        lst3 = []
        lst6 = []
        lst2.append(mid[i].content)

        lst4[i] = lst3
        lst5[i] = lst6
    return render(
        request, 'common/test_selection.html', {
            'manda_mid': json.dumps(lst2, ensure_ascii=False),
            'manda_small': json.dumps(lst4, ensure_ascii=False),
        })
