from django.urls import path
from . import views

app_name = 'mandalart'

urlpatterns = [
    path('plan_big/', views.plan_big, name='plan_big'),
    path('plan_small/', views.plan_small, name='plan_small'),
]