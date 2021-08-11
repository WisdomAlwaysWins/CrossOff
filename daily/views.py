from django.shortcuts import render, redirect
from .models import *
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
from .models import *
from mandalart.models import *
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import resolve_url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
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
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@login_required
def calendar(request, id):
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
        request, 'daily/calendar.html', {
            'manda_mid': json.dumps(lst2, ensure_ascii=False),
            'manda_small': json.dumps(lst4, ensure_ascii=False),
        })
