from django.urls import path
from . import views

app_name = 'admin_hub'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Manajemen Tugas
    path('queue/<int:pk>/allocate/', views.allocate_mechanic, name='allocate_mechanic'),
    path('service/<int:pk>/start/', views.service_start, name='service_start'),
    path('service/<int:pk>/update/', views.service_update, name='service_update'),
    path('service/<int:pk>/finish/', views.service_finish, name='service_finish'),
    
    # Kasir & Pembayaran
    path('payment/<int:pk>/', views.process_payment, name='process_payment'),
    
    # Master Data
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_add, name='service_add'),
    path('mechanics/', views.mechanic_list, name='mechanic_list'),
    
    # Manajemen User (CRUD)
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
]
