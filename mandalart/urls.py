from django.urls import path
from . import views

app_name = 'mandalart'

urlpatterns = [

    path('plan_small/', views.plan_small, name='plan_small'),
    path('new/', views.new, name='new'),
    path('test/', views.test, name='test')
]
