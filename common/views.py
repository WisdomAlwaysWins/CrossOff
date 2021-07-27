from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import *

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('/')
    else:
        form = RegisterForm()
        return render(request, 'common/register.html', {'form' : form})

def login_(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
        return redirect('/')
    else:
        form = LoginForm()
        return render(request, 'common/login.html', {'form':form})

def logout_(request):
    logout(request)
    return redirect('/')

