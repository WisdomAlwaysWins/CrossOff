from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView
from .forms import *
from .models import *
from mandalart.models import *
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
try:
    from django.utils import simplejson as json
except ImportError:
    import json
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
    BigGoalList = []
    if not user.is_manda:
        return redirect('mandalart:new')
    manda = Mandalart.objects.get(user=user.id)
    big = BigGoal.objects.get(manda=manda)
    BigGoalList.append((big.content, big.is_achieved))
    mid = MidGoal.objects.filter(big=big).order_by('id')
    MidGoalList = []
    lst4 = {}
    lst5 = {}
    midcnt = 0
    achieve_spe_num = 0
    for i in range(len(mid)):
        specnt = 0
        lst3 = []
        lst6 = []
        MidGoalList.append(mid[i].content)
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
            'manda': json.dumps(BigGoalList, ensure_ascii=False),
            'manda_mid': json.dumps(MidGoalList, ensure_ascii=False),
            'manda_small': json.dumps(lst4, ensure_ascii=False),
            'manda_small_achieve': json.dumps(lst5, ensure_ascii=False),
            'achieve_num': achieve_num,
            'check_mid_achieve': json.dumps(check_mid_achieve),
            'check_big_achieve': json.dumps(check_big_achieve),
            'todos': json.dumps(todolst, ensure_ascii=False)
        })


@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'common/seeProfile.html', {'user': user})


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
        return render(request, 'common/updateProfile.html', {'user_change_form': user_change_form})


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
    return render(request, 'common/editPassword.html', {'password_change_form': password_change_form})


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


def custom_500_error(request):
    response = render(request, 'errors/500.html')
    response.status_code = 500
    return response


def custom_404_error(request, exception):
    response = render(request, 'errors/404.html')
    response.status_code = 404
    return response


def custom_400_error(request, exception):
    response = render(request, "errors/400.html")
    response.status_code = 400
    return response


@login_required
def selectionForm(request, id):
    user = User.objects.get(id=id)
    if not user.is_manda:
        return redirect('mandalart:new')
    lst = []

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
    return render(
        request, 'common/test_selection.html', {
            'manda_mid': json.dumps(lst2, ensure_ascii=False),
            'manda_small': json.dumps(lst4, ensure_ascii=False),
        })
