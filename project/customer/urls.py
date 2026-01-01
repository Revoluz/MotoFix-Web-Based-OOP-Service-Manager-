from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    # Panel Pelanggan (Customer)
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('motor/add/', views.motor_add, name='motor_add'),
    path('motor/<int:pk>/edit/', views.motor_edit, name='motor_edit'),
    path('motor/<int:pk>/delete/', views.motor_delete, name='motor_delete'),
    path('booking/', views.booking_create, name='booking_create'),
    path('history/', views.service_history, name='service_history'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
]
