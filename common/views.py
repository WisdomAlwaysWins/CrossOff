from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import *
from mandalart.models import *
from django.conf import settings
import json


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
                print(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)
                if remember_session:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                    print(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)
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
    lst.append(big.content)
    mid = MidGoal.objects.filter(big=big)
    lst2 = []
    lst4 = {}
    for i in range(len(mid)):
        lst3 = []
        lst2.append(mid[i].content)
        spe = SpecificGoal.objects.filter(mid=mid[i])
        for j in range(len(spe)):
            lst3.append(spe[j].content)
        lst4[i] = lst3

    achieve_goal = SpecificGoal.objects.filter(is_achieved=True)
    achieve_num = len(achieve_goal)

    check_mid_achieve = []
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
            'manda': json.dumps(lst),
            'manda_mid': json.dumps(lst2),
            'manda_small': json.dumps(lst4),
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
