from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import User
from accounts.views import staff_required, admin_required, cashier_or_admin_required
from customer.models import ServiceBooking, Motor, ServiceType

# Panel Admin & Manajemen (Integrated Hub)
@staff_required
def admin_dashboard(request):
    """Monitoring seluruh antrian & status bengkel"""
    # Statistik booking
    total_bookings = ServiceBooking.objects.count()
    pending_bookings = ServiceBooking.objects.filter(status='pending').count()
    in_progress_bookings = ServiceBooking.objects.filter(status='in_progress').count()
    finished_bookings = ServiceBooking.objects.filter(status='finished').count()
    
    context = {
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'in_progress_bookings': in_progress_bookings,
        'finished_bookings': finished_bookings,
    }
    return render(request, 'admin_hub/dashboard.html', context)

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
    from customer.models import ServiceType
    services = ServiceType.objects.all().order_by('name')
    context = {
        'services': services,
    }
    return render(request, 'admin_hub/service_list.html', context)

@admin_required
def service_add(request):
    """Form tambah jenis layanan baru"""
    from customer.models import ServiceType
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        base_price = request.POST.get('base_price')
        estimated_duration = request.POST.get('estimated_duration')
        
        # Validasi
        if not name or not base_price or not estimated_duration:
            messages.error(request, 'Semua field harus diisi!')
            return render(request, 'admin_hub/service_add.html', {'form_data': request.POST})
        
        try:
            service = ServiceType.objects.create(
                name=name,
                description=description,
                base_price=float(base_price),
                estimated_duration=int(estimated_duration),
                is_active=True
            )
            messages.success(request, f'Layanan "{name}" berhasil ditambahkan!')
            return redirect('admin_hub:service_list')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan layanan: {str(e)}')
            return render(request, 'admin_hub/service_add.html', {
                'form_data': request.POST
            })
    
    return render(request, 'admin_hub/service_add.html')


@admin_required
def service_edit(request, pk):
    """Edit jenis layanan"""
    from customer.models import ServiceType
    service = get_object_or_404(ServiceType, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        base_price = request.POST.get('base_price')
        estimated_duration = request.POST.get('estimated_duration')
        is_active = request.POST.get('is_active') == 'on'
        
        # Validasi
        if not name or not base_price or not estimated_duration:
            messages.error(request, 'Semua field harus diisi!')
            return render(request, 'admin_hub/service_edit.html', {
                'service': service,
            })
        
        try:
            service.name = name
            service.description = description
            service.base_price = float(base_price)
            service.estimated_duration = int(estimated_duration)
            service.is_active = is_active
            service.save()
            messages.success(request, f'Layanan "{name}" berhasil diupdate!')
            return redirect('admin_hub:service_list')
        except Exception as e:
            messages.error(request, f'Gagal mengupdate layanan: {str(e)}')
            return render(request, 'admin_hub/service_edit.html', {
                'service': service,
            })
    
    return render(request, 'admin_hub/service_edit.html', {
        'service': service,
    })

@admin_required
def service_delete(request, pk):
    """Hapus jenis layanan"""
    from customer.models import ServiceType
    service = get_object_or_404(ServiceType, pk=pk)
    
    if request.method == 'POST':
        try:
            # Cek apakah layanan sudah digunakan dalam booking
            if ServiceBooking.objects.filter(service_type=service).exists():
                messages.error(request, 
                    f'Layanan "{service.name}" tidak dapat dihapus karena sudah digunakan dalam booking!')
                return redirect('admin_hub:service_list')
            
            service_name = service.name
            service.delete()
            messages.success(request, f'Layanan "{service_name}" berhasil dihapus!')
        except Exception as e:
            messages.error(request, f'Gagal menghapus layanan: {str(e)}')
        
        return redirect('admin_hub:service_list')
    
    return redirect('admin_hub:service_list')

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
        specialization = request.POST.get('specialization')
        
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
                last_name=last_name,
                specialization=specialization
            )
            messages.success(request, 
                f'User {username} berhasil ditambahkan! '
                f'Username: {username} | Password: {password} '
                f'(Berikan informasi login ini kepada user)')
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
        specialization = request.POST.get('specialization')
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
            user.specialization = specialization
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


# === Manajemen Booking Service ===
@staff_required
def booking_list(request):
    """List semua booking service dengan filter status"""
    status = request.GET.get('status', '')
    
    bookings = ServiceBooking.objects.select_related(
        'customer', 'motor', 'service_type', 'mechanic'
    ).order_by('-booking_date')
    
    if status:
        bookings = bookings.filter(status=status)
    
    context = {
        'bookings': bookings,
        'status_choices': ServiceBooking.STATUS_CHOICES,
        'current_status': status,
        'total_bookings': ServiceBooking.objects.count(),
        'pending_count': ServiceBooking.objects.filter(status='pending').count(),
        'assigned_count': ServiceBooking.objects.filter(status='assigned').count(),
        'in_progress_count': ServiceBooking.objects.filter(status='in_progress').count(),
        'finished_count': ServiceBooking.objects.filter(status='finished').count(),
        'paid_count': ServiceBooking.objects.filter(status='paid').count(),
    }
    
    return render(request, 'admin_hub/booking_list.html', context)


@staff_required
def booking_detail(request, pk):
    """Detail booking service"""
    from customer.models import Invoice
    
    booking = get_object_or_404(ServiceBooking.objects.select_related(
        'customer', 'motor', 'service_type', 'mechanic'
    ).prefetch_related('spare_parts', 'additional_services'), pk=pk)
    
    # include role case-insensitive to avoid missing mechanics due to unexpected role values
    mechanics = User.objects.filter(role__iexact='mechanic').order_by('first_name', 'username')
    
    # Cek apakah invoice sudah ada
    try:
        invoice = Invoice.objects.get(service_booking=booking)
    except Invoice.DoesNotExist:
        invoice = None
    
    context = {
        'booking': booking,
        'mechanics': mechanics,
        'status_choices': ServiceBooking.STATUS_CHOICES,
        'invoice': invoice,
    }
    
    return render(request, 'admin_hub/booking_detail.html', context)


@cashier_or_admin_required
def booking_approve(request, pk):
    """Approve booking (ubah status dari pending ke assigned)"""
    booking = get_object_or_404(ServiceBooking, pk=pk)
    
    if booking.status != 'pending':
        messages.error(request, 'Booking hanya bisa di-approve jika status Menunggu!')
        return redirect('admin_hub:booking_detail', pk=pk)
    
    try:
        booking.status = 'assigned'
        booking.assigned_date = timezone.now()
        booking.save()
        messages.success(request, f'Booking {booking.booking_number} berhasil di-approve!')
        return redirect('admin_hub:booking_detail', pk=pk)
    except Exception as e:
        messages.error(request, f'Gagal approve booking: {str(e)}')
        return redirect('admin_hub:booking_detail', pk=pk)


@cashier_or_admin_required
def booking_assign_mechanic(request, pk):
    """Assign mekanik ke booking"""
    booking = get_object_or_404(ServiceBooking, pk=pk)
    
    if request.method == 'POST':
        mechanic_id = request.POST.get('mechanic_id')
        
        if not mechanic_id:
            messages.error(request, 'Pilih mekanik terlebih dahulu!')
            return redirect('admin_hub:booking_detail', pk=pk)
        
        try:
            # Try to get the user by id first. Avoid failing if role string differs.
            mechanic = User.objects.get(id=mechanic_id)
            if not mechanic.is_mechanic:
                messages.error(request, 'User yang dipilih bukan mekanik. Periksa peran user.')
                return redirect('admin_hub:booking_detail', pk=pk)
            booking.mechanic = mechanic
            booking.status = 'assigned'
            booking.assigned_date = timezone.now()
            booking.save()
            messages.success(request, f'Mekanik {mechanic.get_full_name()} berhasil ditugaskan!')
            return redirect('admin_hub:booking_detail', pk=pk)
        except User.DoesNotExist:
            messages.error(request, 'Mekanik tidak ditemukan!')
            return redirect('admin_hub:booking_detail', pk=pk)
        except Exception as e:
            messages.error(request, f'Gagal assign mekanik: {str(e)}')
            return redirect('admin_hub:booking_detail', pk=pk)
    
    return redirect('admin_hub:booking_detail', pk=pk)


@cashier_or_admin_required
def booking_start(request, pk):
    """Mulai pengerjaan booking"""
    booking = get_object_or_404(ServiceBooking, pk=pk)
    
    if booking.status != 'assigned':
        messages.error(request, 'Booking hanya bisa dimulai jika sudah ditugaskan!')
        return redirect('admin_hub:booking_detail', pk=pk)
    
    try:
        booking.status = 'in_progress'
        booking.start_date = timezone.now()
        booking.save()
        messages.success(request, f'Booking {booking.booking_number} mulai dikerjakan!')
        return redirect('admin_hub:booking_detail', pk=pk)
    except Exception as e:
        messages.error(request, f'Gagal memulai booking: {str(e)}')
        return redirect('admin_hub:booking_detail', pk=pk)


@cashier_or_admin_required
def booking_finish(request, pk):
    """Selesaikan booking"""
    booking = get_object_or_404(ServiceBooking, pk=pk)
    
    if booking.status != 'in_progress':
        messages.error(request, 'Booking hanya bisa diselesaikan jika sedang dikerjakan!')
        return redirect('admin_hub:booking_detail', pk=pk)
    
    try:
        booking.status = 'finished'
        booking.finish_date = timezone.now()
        booking.save()
        messages.success(request, f'Booking {booking.booking_number} telah selesai dikerjakan!')
        return redirect('admin_hub:booking_detail', pk=pk)
    except Exception as e:
        messages.error(request, f'Gagal menyelesaikan booking: {str(e)}')
        return redirect('admin_hub:booking_detail', pk=pk)


@cashier_or_admin_required
def invoice_detail(request, pk):
    """Detail invoice untuk admin/kasir"""
    from customer.models import Invoice, SparePart, AdditionalService
    
    booking = get_object_or_404(ServiceBooking, pk=pk)
    
    # Get invoice
    try:
        invoice = Invoice.objects.get(service_booking=booking)
    except Invoice.DoesNotExist:
        messages.error(request, 'Invoice belum dibuat untuk booking ini!')
        return redirect('admin_hub:booking_detail', pk=pk)
    
    # Get spare parts and additional services
    spare_parts = SparePart.objects.filter(service_booking=booking)
    additional_services = AdditionalService.objects.filter(service_booking=booking)
    
    context = {
        'booking': booking,
        'invoice': invoice,
        'spare_parts': spare_parts,
        'additional_services': additional_services,
    }
    
    return render(request, 'admin_hub/invoice_detail.html', context)


@cashier_or_admin_required
def create_invoice(request, pk):
    """Buat invoice untuk booking yang sudah selesai"""
    from customer.models import Invoice, SparePart, AdditionalService
    from decimal import Decimal
    
    booking = get_object_or_404(ServiceBooking, pk=pk)
    
    # Cek apakah booking sudah selesai atau paid
    if booking.status not in ['finished', 'paid']:
        messages.error(request, 'Invoice hanya bisa dibuat untuk booking yang sudah selesai!')
        return redirect('admin_hub:booking_detail', pk=pk)
    
    # Cek apakah invoice sudah ada
    try:
        existing_invoice = Invoice.objects.get(service_booking=booking)
        messages.warning(request, 'Invoice sudah dibuat sebelumnya!')
        return redirect('admin_hub:booking_detail', pk=pk)
    except Invoice.DoesNotExist:
        pass
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'cash')
        paid_amount_str = request.POST.get('paid_amount', '0')
        
        try:
            # Hitung biaya layanan dasar
            service_cost = Decimal(str(booking.service_type.base_price))
            
            # Hitung total biaya suku cadang
            spare_parts = SparePart.objects.filter(service_booking=booking)
            spare_parts_cost = sum(Decimal(str(sp.price * sp.quantity)) for sp in spare_parts)
            
            # Hitung total biaya jasa tambahan
            additional_services = AdditionalService.objects.filter(service_booking=booking)
            additional_cost = sum(Decimal(str(ads.price)) for ads in additional_services)
            
            # Total biaya
            total_cost = service_cost + spare_parts_cost + additional_cost
            
            # Parse paid amount dari form
            paid_amount = Decimal(str(paid_amount_str))
            
            # Validasi pembayaran
            if paid_amount < total_cost:
                messages.error(request, f'Uang yang dibayarkan kurang! Total: Rp {total_cost:,.0f}, Dibayar: Rp {paid_amount:,.0f}')
                return redirect('admin_hub:booking_detail', pk=pk)
            
            # Hitung kembalian
            change_amount = paid_amount - total_cost
            
            # Buat invoice
            invoice = Invoice.objects.create(
                service_booking=booking,
                invoice_number=f"INV-{booking.booking_number}",
                service_cost=service_cost,
                spare_parts_cost=spare_parts_cost,
                additional_cost=additional_cost,
                total_cost=total_cost,
                payment_method=payment_method,
                paid_amount=paid_amount,
                change_amount=change_amount,
                cashier=request.user
            )
            
            # Update status booking menjadi paid jika belum
            if booking.status == 'finished':
                booking.status = 'paid'
                booking.save()
            
            messages.success(request, 
                f'Invoice {invoice.invoice_number} berhasil dibuat! '
                f'Total: Rp {total_cost:,.0f} | Dibayar: Rp {paid_amount:,.0f} | Kembalian: Rp {change_amount:,.0f}')
            return redirect('admin_hub:booking_detail', pk=pk)
            
        except Exception as e:
            messages.error(request, f'Gagal membuat invoice: {str(e)}')
            return redirect('admin_hub:booking_detail', pk=pk)
    
    return redirect('admin_hub:booking_detail', pk=pk)


@cashier_or_admin_required
def booking_cancel(request, pk):
    """Batalkan booking"""
    booking = get_object_or_404(ServiceBooking, pk=pk)
    
    if booking.status in ['finished', 'paid', 'cancelled']:
        messages.error(request, f'Booking dengan status {booking.get_status_display()} tidak bisa dibatalkan!')
        return redirect('admin_hub:booking_detail', pk=pk)
    
    if request.method == 'POST':
        try:
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, f'Booking {booking.booking_number} berhasil dibatalkan!')
            return redirect('admin_hub:booking_list')
        except Exception as e:
            messages.error(request, f'Gagal membatalkan booking: {str(e)}')
            return redirect('admin_hub:booking_detail', pk=pk)
    
    return render(request, 'admin_hub/booking_cancel.html', {'booking': booking})


@cashier_or_admin_required
def booking_create(request):
    """Buat booking baru (walk-in)"""
    motors = Motor.objects.select_related('owner').all()
    service_types = ServiceType.objects.filter(is_active=True)
    from accounts.models import User
    customers = User.objects.filter(role='customer')
    
    if request.method == 'POST':
        motor_id = request.POST.get('motor_id')
        customer_id = request.POST.get('customer_id')
        guest_name = request.POST.get('guest_name', '').strip()
        guest_phone = request.POST.get('guest_phone', '').strip()
        
        # Walk-in motor fields
        motor_license_plate = request.POST.get('motor_license_plate', '').strip()
        motor_brand = request.POST.get('motor_brand', '').strip()
        motor_model = request.POST.get('motor_model', '').strip()
        motor_year = request.POST.get('motor_year', '').strip()
        
        service_type_id = request.POST.get('service_type_id')
        complaint = request.POST.get('complaint')
        notes = request.POST.get('notes', '')

        # Validasi: harus ada service_type dan complaint
        if not service_type_id or not complaint:
            messages.error(request, 'Mohon isi jenis layanan dan keluhan pelanggan!')
            return render(request, 'admin_hub/booking_create.html', {
                'motors': motors,
                'service_types': service_types,
                'customers': customers,
                'form_data': request.POST,
            })

        try:
            # === 1. Tentukan Customer ===
            if customer_id:
                # Pelanggan terdaftar
                customer = User.objects.get(id=customer_id)
                guest_password = None
            else:
                # Pelanggan walk-in: buat user guest
                if not guest_name or not guest_phone:
                    raise ValueError('Untuk pelanggan walk-in, mohon isi nama dan nomor telepon!')
                
                # Generate unique username yang lebih pendek
                import time, random, string
                # Ambil 4 digit terakhir nomor telepon
                phone_digits = ''.join(ch for ch in guest_phone if ch.isdigit())
                last_digits = phone_digits[-4:] if len(phone_digits) >= 4 else phone_digits
                # Generate 3 digit random
                random_suffix = ''.join(random.choices(string.digits, k=3))
                uname = f"guest{last_digits}{random_suffix}"
                
                # Pastikan unique
                counter = 1
                base_uname = uname
                while User.objects.filter(username=uname).exists():
                    uname = f"{base_uname}{counter}"
                    counter += 1
                
                # Generate random password (8 karakter)
                guest_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                
                customer = User.objects.create_user(
                    username=uname,
                    password=guest_password,  # Set password agar bisa login
                    role='customer',
                    first_name=guest_name,
                    phone=guest_phone,
                )
                customer.save()

            # === 2. Tentukan Motor ===
            if motor_id:
                # Motor dari database
                motor = Motor.objects.get(id=motor_id)
            else:
                # Motor walk-in: input manual
                if not motor_license_plate or not motor_brand or not motor_model:
                    raise ValueError('Untuk motor walk-in, mohon isi plat nomor, merk, dan model!')
                
                if not motor_year:
                    motor_year = timezone.now().year
                
                # Cek apakah motor dengan plat nomor ini sudah ada
                motor, created = Motor.objects.get_or_create(
                    license_plate=motor_license_plate.upper(),
                    defaults={
                        'owner': customer,
                        'brand': motor_brand,
                        'model': motor_model,
                        'year': int(motor_year) if motor_year else timezone.now().year,
                    }
                )
                
                if not created:
                    # Motor sudah ada, update owner jika berbeda
                    if motor.owner != customer:
                        motor.owner = customer
                        motor.save()

            # === 3. Buat Booking ===
            service_type = ServiceType.objects.get(id=service_type_id)

            booking = ServiceBooking.objects.create(
                motor=motor,
                customer=customer,
                service_type=service_type,
                complaint=complaint,
                notes=notes,
                booking_type='walk_in',
                status='pending'
            )

            # Success message dengan info login untuk guest user
            if guest_password:
                messages.success(request, 
                    f'Booking {booking.booking_number} berhasil dibuat! '
                    f'Akun pelanggan dibuat: Username: {customer.username} | Password: {guest_password} '
                    f'(Berikan informasi login ini kepada pelanggan)')
            else:
                messages.success(request, f'Booking {booking.booking_number} berhasil dibuat! Motor: {motor.license_plate}')
            
            return redirect('admin_hub:booking_detail', pk=booking.pk)
            
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'admin_hub/booking_create.html', {
                'motors': motors,
                'service_types': service_types,
                'customers': customers,
                'form_data': request.POST,
            })
        except Exception as e:
            messages.error(request, f'Gagal membuat booking: {str(e)}')
            return render(request, 'admin_hub/booking_create.html', {
                'motors': motors,
                'service_types': service_types,
                'customers': customers,
                'form_data': request.POST,
            })
    
    context = {
        'motors': motors,
        'service_types': service_types,
        'customers': customers,
    }
    
    return render(request, 'admin_hub/booking_create.html', context)


@cashier_or_admin_required
def booking_update_status(request, pk):
    """Update status booking"""
    booking = get_object_or_404(ServiceBooking, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        # Validasi status transition
        valid_transitions = {
            'pending': ['assigned', 'cancelled'],
            'assigned': ['in_progress', 'cancelled'],
            'in_progress': ['finished', 'cancelled'],
            'finished': ['paid'],
            'paid': [],
            'cancelled': [],
        }
        
        if new_status not in valid_transitions.get(booking.status, []):
            messages.error(request, f'Transisi status dari {booking.get_status_display()} ke {new_status} tidak diizinkan!')
            return redirect('admin_hub:booking_detail', pk=pk)
        
        try:
            booking.status = new_status
            
            # Update timestamp sesuai status
            if new_status == 'assigned' and not booking.assigned_date:
                booking.assigned_date = timezone.now()
            elif new_status == 'in_progress' and not booking.start_date:
                booking.start_date = timezone.now()
            elif new_status == 'finished' and not booking.finish_date:
                booking.finish_date = timezone.now()
            elif new_status == 'paid' and not booking.payment_date:
                booking.payment_date = timezone.now()
            
            booking.save()
            messages.success(request, f'Status booking berhasil diubah menjadi {booking.get_status_display()}!')
            return redirect('admin_hub:booking_detail', pk=pk)
        except Exception as e:
            messages.error(request, f'Gagal update status: {str(e)}')
            return redirect('admin_hub:booking_detail', pk=pk)
    
    return redirect('admin_hub:booking_detail', pk=pk)
