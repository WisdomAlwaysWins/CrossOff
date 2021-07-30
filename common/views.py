from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from mandalart.models import *


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('mandalart:new')
    else:
        form = RegisterForm()
        return render(request, 'common/register.html', {'form': form})


def login_(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request,
                                username=username,
                                password=password)
            if user is not None:
                login(request, user)
                return redirect('mandalart:new')
        return redirect('home:main')
    else:
        form = LoginForm()
        return render(request, 'common/login.html', {'form': form})


def logout_(request):
    logout(request)
    return redirect('home:main')


@login_required
def dashboard(request, id):
    user = User.objects.get(id=id)
    lst = []
    manda = Mandalart.objects.get(user=request.user.id)
    big = BigGoal.objects.get(manda=manda)
    lst.append(big.content)
    mid = MidGoal.objects.filter(big=big)
    lst2 = []
    lst4 ={}
    for i in range(len(mid)):
        lst3 = []  
        lst2.append(mid[i].content)
        spe = SpecificGoal.objects.filter(mid=mid[i])
        for j in range(len(spe)):
            lst3.append(spe[j].content)
        lst4[i] = lst3
    return render(request, 'common/dashboard.html', {'user': user, 'manda': lst, 'manda_mid':lst2, 'manda_small' : lst4})

