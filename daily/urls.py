from os import name
from django.urls import path
from . import views

app_name = 'daily'

urlpatterns = [
    path('calendar/<str:id>', views.calendar, name='calendar'),
    path('calendar/add/Block', views.addBlock, name='addblock'),
]
