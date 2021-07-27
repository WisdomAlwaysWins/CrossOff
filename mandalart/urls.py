from django.urls import path
from . import views

app_name = 'mandalart'

urlpatterns = [
    path('new/', views.new, name='new'),
    path('test/', views.test, name='test')
]
