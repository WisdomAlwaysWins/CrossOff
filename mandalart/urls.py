from django.urls import path
from . import views

app_name = 'mandalart'

urlpatterns = [
    path('', views.new, name='new'),
]