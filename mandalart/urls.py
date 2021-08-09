from django.urls import path
from . import views

app_name = 'mandalart'

urlpatterns = [
    path('plan_small/', views.plan_small, name='plan_small'),
    path('new/', views.new, name='new'),
    path('test/', views.test, name='test'),
    path('delete/', views.delMandalart, name='delete'),
    path('edit/', views.editMandalart, name='edit'),
    path('addTodo/', views.addTodo, name='addTodo'),
    path('delTodo/<int:id>', views.delTodo, name='delTodo'),
    path('share/<str:id>', views.shareManda, name='share'),
]
