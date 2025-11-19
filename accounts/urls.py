from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/create', views.create_user, name='new_user'),
    path('departments', views.department_list, name='department_list'),
    path('departments/create', views.create_department, name='new_department'),
    path('roles/', views.roles, name='role_list'),
    path('roles/create', views.create_role, name='new_role'),
]