from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    path('', views.tickets, name='tickets_list'),
    path('create/', views.create_ticket, name='create_ticket'),
]
