from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    Custom User Model untuk MotoFix
    Extends Django AbstractUser untuk menambahkan field tambahan
    """
    ROLE_CHOICES = (
        ('customer', 'Pelanggan'),
        ('mechanic', 'Mekanik'),
        ('cashier', 'Kasir'),
        ('admin', 'Admin'),
    )
    
    SPECIALIZATION_CHOICES = (
        ('umum', 'Umum'),
        ('mesin', 'Mesin'),
        ('elektrikal', 'Elektrikal'),
        ('ban', 'Ban'),
        ('transmisi', 'Transmisi'),
        ('suspensi', 'Suspensi'),
        ('rem', 'Rem'),
        ('karburator', 'Karburator/Injeksi'),
        ('rantai_sproket', 'Rantai dan Sproket'),
        ('kopling', 'Kopling'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, default='umum', blank=True, null=True, verbose_name='Spesialisasi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_customer(self):
        return self.role == 'customer'
    
    @property
    def is_mechanic(self):
        return self.role == 'mechanic'
    
    @property
    def is_cashier(self):
        return self.role == 'cashier'
    
    @property
    def is_admin_user(self):
        return self.role == 'admin'
