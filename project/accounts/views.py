from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps
from .models import User

# Decorator untuk cek role
def customer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_customer:
            messages.error(request, 'Akses ditolak! Halaman ini khusus untuk pelanggan.')
            return redirect('admin_hub:admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.is_customer:
            messages.error(request, 'Akses ditolak! Halaman ini khusus untuk staff.')
            return redirect('customer:customer_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_admin_user:
            messages.error(request, 'Akses ditolak! Halaman ini khusus untuk admin.')
            return redirect('admin_hub:admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

# Autentikasi & Akun
def login(request):
    """Halaman login untuk semua user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Selamat datang, {user.username}!')
            
            # Redirect berdasarkan role
            if user.is_admin_user or user.is_cashier or user.is_mechanic:
                return redirect('admin_hub:admin_dashboard')
            else:
                return redirect('customer:customer_dashboard')
        else:
            messages.error(request, 'Username atau password salah!')
    
    return render(request, 'accounts/login.html')

def logout(request):
    """Proses logout"""
    auth_logout(request)
    messages.info(request, 'Anda telah logout.')
    return redirect('accounts:login')

def register(request):
    """Halaman pendaftaran pelanggan baru"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        # Validasi
        if password != password_confirm:
            messages.error(request, 'Password tidak sama!')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan!')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar!')
            return render(request, 'accounts/register.html')
        
        # Buat user baru
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='customer',
                phone=phone,
                address=address
            )
            messages.success(request, 'Registrasi berhasil! Silakan login.')
            return redirect('accounts:login')
        except Exception as e:
            messages.error(request, f'Registrasi gagal: {str(e)}')
    
    return render(request, 'accounts/register.html')
