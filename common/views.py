from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import *
from mandalart.models import *
from django.contrib import messages


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
                return redirect('mandalart:new')
        else:
            return redirect('common:fail')

    else:
        form = LoginForm()
        return render(request, 'common/login.html', {'form': form})


def fail(request):
    return render(request, 'common/login_fail.html')


def logout_(request):
    logout(request)
    return redirect('home:home')


@login_required
def dashboard(request, id):
    user = User.objects.get(id=id)
    lst = []
    manda = Mandalart.objects.get(user=user.id)
    big = BigGoal.objects.get(manda=manda)
    lst.append(big.content)
    mid = MidGoal.objects.filter(big=big)
    for i in range(len(mid)):
        lst2 = []
        lst3 = []
        lst2.append(mid[i].content)
        spe = SpecificGoal.objects.filter(mid=mid[i])
        for j in range(len(spe)):
            lst3.append(spe[j].content)
        lst2.append(lst3)
        lst.append(lst2)
    return render(request, 'common/dashboard.html', {'user': user, 'manda': lst})


def profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'common/seeProfile.html', {'user': user})


def profileUpdate(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(
            request.POST, instance=request.user)

        if user_change_form.is_valid():
            user_change_form.save()
            return render(request, 'common/dashboard.html')
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        return render(request, 'common/updateProfile.html', {'user_change_form': user_change_form})


def passwordEdit(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(
            request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호 변경 완료!')
            return render(request, 'common/dashboard.html')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)
    return render(request, 'common/editPassword.html', {'password_change_form': password_change_form})
