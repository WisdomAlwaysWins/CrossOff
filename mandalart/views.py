from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *


@login_required
def new(request):
    if request.method == 'POST':
        u = request.user
        print(u)
        a = Mandalart(user=u)
        a.save()
        b = BigGoal(manda=a, content=request.POST['big'])
        b.save()
        for i in range(1, 9):
            c = 'mid' + str(i)
            MidGoal(big=b, content=request.POST[c]).save()
        return redirect('home:main')
    else:
        return render(request, 'mandalart/new.html')


@login_required
def show(request):
    pass