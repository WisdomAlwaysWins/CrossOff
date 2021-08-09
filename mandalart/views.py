from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
import json


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
        return redirect('mandalart:plan_small')

    else:
        u = request.user
        if (u.is_manda):
            return redirect('/common/dashboard/' + str(u.id))
        return render(request, 'mandalart/plan_big.html')


@login_required
def plan_small(request):
    if request.method == 'POST':
        a = Mandalart.objects.get(user=request.user.id)
        b = BigGoal.objects.get(manda=a)
        m = MidGoal.objects.filter(big=b)
        for i in range(len(m)):
            for j in range(0, 8):
                s = SpecificGoal(mid=m[i],
                                 content=request.POST['box' + str(i) + str(j)])
                s.save()
        return redirect('/common/dashboard/' + str(request.user.id))
    else:
        lst = []
        manda = Mandalart.objects.get(user=request.user.id)
        big = BigGoal.objects.get(manda=manda)
        lst.append(big.content)
        mid = MidGoal.objects.filter(big=big).order_by('id')
        lst2 = []
        for i in range(len(mid)):
            lst2.append(mid[i].content)
        lst.append(lst2)
        return render(request, 'mandalart/plan_small.html',
                      {'manda': json.dumps(lst, ensure_ascii=False)})


@login_required
def test(request):
    lst = []
    manda = Mandalart.objects.get(user=request.user.id)
    big = BigGoal.objects.get(manda=manda)
    lst.append(big.content)
    mid = MidGoal.objects.filter(big=big).order_by('id')
    for i in range(len(mid)):
        lst2 = []
        lst3 = []
        lst2.append(mid[i].content)
        spe = SpecificGoal.objects.filter(mid=mid[i]).order_by('id')
        for j in range(len(spe)):
            lst3.append(spe[j].content)
        lst2.append(lst3)
        lst.append(lst2)
    return render(request, 'mandalart/test.html', {'manda': lst})


@login_required
def delMandalart(request):
    manda = Mandalart.objects.get(user=request.user.id)
    manda.delete()
    request.user.is_manda = False
    request.user.save()
    return redirect('mandalart:new')


@login_required
def editMandalart(request):
    bigcontent = ''
    midlst = []
    spelst = {}
    achievedlst = {}
    for i in range(1, 10):
        t = []
        t2 = []
        for j in range(1, 10):
            if i == 5:
                if not j == 5:
                    midlst.append(request.POST['box' + str(i) + str(j)])
                if j == 5:
                    bigcontent = request.POST['box55']
            else:
                if j == 5:
                    continue
                t.append(request.POST['box' + str(i) + str(j)])
                t2.append(request.POST.get('chk' + str(i) + str(j), False))
            if i <= 5:
                spelst[i] = t
                achievedlst[i] = t2
            else:
                spelst[i - 1] = t
                achievedlst[i - 1] = t2

    manda = Mandalart.objects.get(user=request.user.id)
    big = BigGoal.objects.get(manda=manda)
    if (bigcontent != big.content):
        big.content = bigcontent
        big.save()
    mids = MidGoal.objects.filter(big=big).order_by('id')
    for i in range(len(mids)):
        spes = SpecificGoal.objects.filter(mid=mids[i]).order_by('id')
        if mids[i].content != midlst[i]:
            mids[i].content = midlst[i]
            mids[i].save()
        for j in range(len(spes)):
            spes[j].is_achieved = achievedlst[i + 1][j]
            if spes[j].content != spelst[i + 1][j]:
                spes[j].content = spelst[i + 1][j]
            spes[j].save()

    return redirect('/common/dashboard/' + str(request.user.id))


@login_required
def addTodo(request):
    u = request.user
    newTodo = Todo(user=u)
    newTodo.content = request.POST['todoInput']
    newTodo.save()
    return redirect('/common/dashboard/' + str(request.user.id))


@login_required
def delTodo(request, id):
    u = request.user
    deltodo = Todo.objects.get(user=u, id=id)
    deltodo.delete()
    return redirect('/common/dashboard/' + str(request.user.id))


def shareManda(request, id):
    u = User.objects.get(id=id)
    manda = Mandalart.objects.get(user=u)
    lst = []
    big = BigGoal.objects.get(manda=manda)
    lst.append(big.content)
    mid = MidGoal.objects.filter(big=big).order_by('id')
    for i in range(len(mid)):
        lst2 = []
        lst3 = []
        lst2.append(mid[i].content)
        spe = SpecificGoal.objects.filter(mid=mid[i]).order_by('id')
        for j in range(len(spe)):
            lst3.append(spe[j].content)
        lst2.append(lst3)
        lst.append(lst2)
    return render(request, 'mandalart/share_manda.html', {
        'manda': json.dumps(lst, ensure_ascii=False),
        'nickname': u.nickname
    })
