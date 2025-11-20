from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    path('', views.tickets, name='tickets_list'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('ticket_list/', views.tickets, name='ticket_list'),
    path('assign/<int:ticket_id>/', views.assign_ticket, name='assign_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_details, name='ticket_details'),
    path('ticket/status/', views.status, name='status'),
]
