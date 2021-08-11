"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import common.views as cv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('common/', include('common.urls')),
    path('', include('home.urls')),
    path('mandalart/', include('mandalart.urls')),
    path('daily/', include('daily.urls')),
    # path('password_reset/', cv.password_reset, name="password_reset"),
    # path('password_reset_done/', cv.password_reset_done, name="password_reset_done"),
    # path('password_reset_done_fail/', cv.password_reset_done_fail, name="password_reset_done_fial"),
    # path('password_reset_confirm/', cv.password_reset_confirm, name="password_reset_confirm"),
    # path('password_reset_complete/', cv.password_reset_complete, name="password_reset_complete"),

    path('password_reset/', cv.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', cv.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', cv.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', cv.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
