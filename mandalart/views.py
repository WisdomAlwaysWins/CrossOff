from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *


@login_required
def new(request):
    if request.method == 'POST':
        u = request.user
        a = Mandalart(user=u)
        u.is_manda = True
        a.save()
        u.save()
        b = BigGoal(manda=a, content=request.POST['big'])
        b.save()
        for i in range(1, 9):
            c = 'mid' + str(i)
            MidGoal(big=b, content=request.POST[c]).save()
        return redirect('/common/dashboard/' + str(u.id))
    else:
        u = request.user
        if(u.is_manda):
            return redirect('/common/dashboard/' + str(u.id))
        return render(request, 'mandalart/plan_big.html')


def plan_small(request):
    return render(request, 'mandalart/plan_small.html')


@login_required
def test(request):
    lst = []
    manda = Mandalart.objects.get(user=request.user.id)
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
    return render(request, 'mandalart/test.html', {'manda': lst})

@login_required
def mid(request):
    lst = []
    manda = Mandalart.objects.get(user=request.user.id)
    big = BigGoal.objects.get(manda=manda)
    mid = MidGoal.objects.filter(big=big)
    for i in range(len(mid)):
        lst.append(mid[i].content)
    return render(request, 'mandalart/test.html', {'manda_mid': lst})
