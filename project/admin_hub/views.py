from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from accounts.views import staff_required, admin_required

# Panel Admin & Manajemen (Integrated Hub)
@admin_required
def admin_dashboard(request):
    """Monitoring seluruh antrian & status bengkel"""
    return render(request, 'admin_hub/dashboard.html')

# === Manajemen Tugas ===
@admin_required
def allocate_mechanic(request, pk):
    """Proses admin menugaskan mekanik"""
    return render(request, 'admin_hub/allocate_mechanic.html', {'pk': pk})

@admin_required
def service_start(request, pk):
    """Trigger mekanik mulai bekerja (via Admin)"""
    return render(request, 'admin_hub/service_start.html', {'pk': pk})

@admin_required
def service_update(request, pk):
    """Input suku cadang & jasa tambahan (Modal)"""
    return render(request, 'admin_hub/service_update.html', {'pk': pk})

@admin_required
def service_finish(request, pk):
    """Menandai pengerjaan mekanik selesai"""
    return render(request, 'admin_hub/service_finish.html', {'pk': pk})

# === Kasir & Pembayaran ===
@admin_required
def process_payment(request, pk):
    """Form kasir untuk konfirmasi pembayaran"""
    return render(request, 'admin_hub/process_payment.html', {'pk': pk})

# === Master Data ===
@admin_required
def service_list(request):
    """List semua jenis layanan (Master Data)"""
    return render(request, 'admin_hub/service_list.html')

@admin_required
def service_add(request):
    """Form tambah jenis layanan baru"""
    return render(request, 'admin_hub/service_add.html')

@admin_required
def mechanic_list(request):
    """List data mekanik"""
    mechanics = User.objects.filter(role='mechanic')
    return render(request, 'admin_hub/mechanic_list.html', {'mechanics': mechanics})

# === Manajemen User (CRUD) ===
@admin_required
def user_list(request):
    """List semua user"""
    users = User.objects.all().order_by('-created_at')
    return render(request, 'admin_hub/user_list.html', {'users': users})

@admin_required
def user_create(request):
    """Form tambah user baru"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        role = request.POST.get('role')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Validasi
        if password != password_confirm:
            messages.error(request, 'Password tidak sama!')
            return render(request, 'admin_hub/user_form.html', {
                'form_data': request.POST,
                'action': 'create'
            })
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan!')
            return render(request, 'admin_hub/user_form.html', {
                'form_data': request.POST,
                'action': 'create'
            })
        
        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar!')
            return render(request, 'admin_hub/user_form.html', {
                'form_data': request.POST,
                'action': 'create'
            })
        
        # Buat user baru
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                phone=phone,
                address=address,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, f'User {username} berhasil ditambahkan!')
            return redirect('admin_hub:user_list')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan user: {str(e)}')
    
    return render(request, 'admin_hub/user_form.html', {'action': 'create'})

@admin_required
def user_detail(request, pk):
    """Detail user"""
    user = get_object_or_404(User, pk=pk)
    return render(request, 'admin_hub/user_detail.html', {'user_obj': user})

@admin_required
def user_update(request, pk):
    """Form edit user"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_active = request.POST.get('is_active') == 'on'
        
        # Validasi username unique (kecuali user sendiri)
        if username != user.username and User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan!')
            return render(request, 'admin_hub/user_form.html', {
                'user_obj': user,
                'action': 'update'
            })
        
        # Validasi email unique (kecuali user sendiri)
        if email and email != user.email and User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar!')
            return render(request, 'admin_hub/user_form.html', {
                'user_obj': user,
                'action': 'update'
            })
        
        # Update user
        try:
            user.username = username
            user.email = email
            user.role = role
            user.phone = phone
            user.address = address
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = is_active
            
            # Update password jika diisi
            new_password = request.POST.get('password')
            if new_password:
                password_confirm = request.POST.get('password_confirm')
                if new_password != password_confirm:
                    messages.error(request, 'Password tidak sama!')
                    return render(request, 'admin_hub/user_form.html', {
                        'user_obj': user,
                        'action': 'update'
                    })
                user.set_password(new_password)
            
            user.save()
            messages.success(request, f'User {username} berhasil diupdate!')
            return redirect('admin_hub:user_detail', pk=user.pk)
        except Exception as e:
            messages.error(request, f'Gagal mengupdate user: {str(e)}')
    
    return render(request, 'admin_hub/user_form.html', {
        'user_obj': user,
        'action': 'update'
    })

@admin_required
def user_delete(request, pk):
    """Hapus user"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = user.username
        try:
            user.delete()
            messages.success(request, f'User {username} berhasil dihapus!')
            return redirect('admin_hub:user_list')
        except Exception as e:
            messages.error(request, f'Gagal menghapus user: {str(e)}')
            return redirect('admin_hub:user_detail', pk=pk)
    
    return render(request, 'admin_hub/user_delete.html', {'user_obj': user})
