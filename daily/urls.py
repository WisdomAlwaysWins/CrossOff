from os import name
from django.urls import path
from . import views

app_name = 'daily'

urlpatterns = [
    path('calendar/<str:id>', views.calendar, name='calendar'),
    path('calendar/block/add', views.addBlock, name='addblock'),
    path('calendar/block/delete/<str:date>', views.delBlock, name='delblock')
]
