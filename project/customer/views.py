from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from accounts.views import customer_required
from .models import Motor, ServiceType, ServiceBooking, Invoice
import random

# Panel Pelanggan (Customer)
@customer_required
def customer_dashboard(request):
    """Dashboard utama & tracking status aktif"""
    # Get customer's motors
    motors = Motor.objects.filter(owner=request.user)
    
    # Get active bookings (not paid or cancelled)
    active_bookings = ServiceBooking.objects.filter(
        customer=request.user
    ).exclude(
        status__in=['paid', 'cancelled']
    ).select_related('motor', 'service_type', 'mechanic').order_by('-booking_date')[:5]
    
    # Get recent completed services
    completed_services = ServiceBooking.objects.filter(
        customer=request.user,
        status__in=['paid', 'finished']
    ).select_related('motor', 'service_type').order_by('-finish_date')[:3]
    
    context = {
        'motors': motors,
        'motors_count': motors.count(),
        'active_bookings': active_bookings,
        'active_bookings_count': active_bookings.count(),
        'completed_services': completed_services,
        'total_services': ServiceBooking.objects.filter(customer=request.user).count(),
    }
    
    return render(request, 'customer/dashboard.html', context)

@customer_required
def motor_add(request):
    """Form tambah motor baru"""
    if request.method == 'POST':
        try:
            # Get form data
            license_plate = request.POST.get('license_plate', '').strip().upper()
            brand = request.POST.get('brand', '').strip()
            model = request.POST.get('model', '').strip()
            year = request.POST.get('year', '').strip()
            
            print(request.POST)
            # engine_number = request.POST.get('engine_number', '').strip()
            # frame_number = request.POST.get('frame_number', '').strip()
            # notes = request.POST.get('notes', '').strip()
            
            # Validation
            if not all([license_plate, brand, model, year]):
                messages.error(request, 'Plat nomor`, merk, model, tahun, dan warna harus diisi!')
                return render(request, 'customer/dashboard.html', {'post_data': request.POST})
            
            # Check if license plate already exists
            if Motor.objects.filter(license_plate=license_plate).exists():
                messages.error(request, f'Motor dengan plat nomor {license_plate} sudah terdaftar!')
                return render(request, 'customer/motor_add.html', {'post_data': request.POST})
            
            # Validate year
            try:
                year_int = int(year)
                if year_int < 1900 or year_int > timezone.now().year + 1:
                    messages.error(request, 'Tahun motor tidak valid!')
                    return render(request, 'customer/motor_add.html', {'post_data': request.POST})
            except ValueError:
                messages.error(request, 'Tahun harus berupa angka!')
                return render(request, 'customer/motor_add.html', {'post_data': request.POST})
            print(request.user)
            # Create motor
            motor = Motor.objects.create(
                owner=request.user,
                license_plate=license_plate,
                brand=brand,
                model=model,
                year=year_int,
            )
            
            messages.success(request, f'Motor {motor.license_plate} berhasil ditambahkan!')
            return redirect('customer:customer_dashboard')
            
        except Exception as e:
            messages.error(request, f'Gagal menambahkan motor: {str(e)}')
            return render(request, 'customer/motor_add.html', {'post_data': request.POST})
    
    return render(request, 'customer/motor_add.html')

@customer_required
def motor_edit(request, pk):
    """Form edit data motor"""
    motor = get_object_or_404(Motor, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        try:
            # Get form data
            license_plate = request.POST.get('license_plate', '').strip().upper()
            brand = request.POST.get('brand', '').strip()
            model = request.POST.get('model', '').strip()
            year = request.POST.get('year', '').strip()
            
            # Validation
            if not all([license_plate, brand, model, year]):
                messages.error(request, 'Plat nomor,  model, dan tahun harus diisi!')
                print(license_plate, brand, model, year)
                return render(request, 'customer/motor_edit.html', {'motor': motor})
            
            # Check if license plate already exists (except current motor)
            if Motor.objects.filter(license_plate=license_plate).exclude(pk=motor.pk).exists():
                messages.error(request, f'Motor dengan plat nomor {license_plate} sudah terdaftar!')
                return render(request, 'customer/motor_edit.html', {'motor': motor})
            
            # Validate year
            try:
                year_int = int(year)
                if year_int < 1900 or year_int > timezone.now().year + 1:
                    messages.error(request, 'Tahun motor tidak valid!')
                    return render(request, 'customer/motor_edit.html', {'motor': motor})
            except ValueError:
                messages.error(request, 'Tahun harus berupa angka!')
                return render(request, 'customer/motor_edit.html', {'motor': motor})
            
            # Update motor
            motor.license_plate = license_plate
            motor.brand = brand
            motor.model = model
            motor.year = year_int

            motor.save()
            
            messages.success(request, f'Data motor {motor.license_plate} berhasil diupdate!')
            return redirect('customer:customer_dashboard')
            
        except Exception as e:
            messages.error(request, f'Gagal mengupdate motor: {str(e)}')
    
    return render(request, 'customer/motor_edit.html', {'motor': motor})

@customer_required
def motor_delete(request, pk):
    """Hapus motor"""
    motor = get_object_or_404(Motor, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        try:
            motor.delete()
            messages.success(request, f'Motor {motor.license_plate} berhasil dihapus!')
            return redirect('customer:customer_dashboard')
        except Exception as e:
            messages.error(request, f'Gagal menghapus motor: {str(e)}')
            return redirect('customer:customer_dashboard')
    
    return render(request, 'customer/motor_delete_confirm.html', {'motor': motor})

@customer_required
def booking_create(request):
    """Form buat antrian (Booking/Walk-in)"""
    # Get customer's motors
    motors = Motor.objects.filter(owner=request.user)
    
    # Get active service types
    service_types = ServiceType.objects.filter(is_active=True)
    
    if request.method == 'POST':
        try:
            # Get form data
            print(request.POST)
            motor_id = request.POST.get('motor')
            first_name = request.POST.get('first_name', '').strip()
            service_type_id = request.POST.get('service')
            complaint = request.POST.get('complaint', '').strip()
            booking_type = request.POST.get('booking_type', 'booking')
            
            # Validation
            if not all([motor_id, service_type_id, complaint, booking_type]):
                messages.error(request, 'Motor, jenis servis, dan keluhan harus diisi!')
                return render(request, 'customer/booking_create.html', {
                    'motors': motors,
                    'service_types': service_types,
                    'post_data': request.POST,
                    'booking_type': booking_type,
                })
            
            # Get motor and service type
            motor = get_object_or_404(Motor, pk=motor_id, owner=request.user)
            service_type = get_object_or_404(ServiceType, pk=service_type_id, is_active=True)
            
            # Generate booking number (format: BK-YYYYMMDD-XXXX)
            today = timezone.now()
            date_str = today.strftime('%Y%m%d')
            random_num = random.randint(1000, 9999)
            booking_number = f'BK-{date_str}-{random_num}'
            
            
            # Make sure booking number is unique
            while ServiceBooking.objects.filter(booking_number=booking_number).exists():
                random_num = random.randint(1000, 9999)
                booking_number = f'BK-{date_str}-{random_num}'
                
            while ServiceBooking.objects.filter(motor=motor, status__in=['pending', 'in_progress']).exists():
                messages.error(request, f'Motor {motor.license_plate} sudah memiliki booking aktif!')
                return render(request, 'customer/booking_create.html', {
                    'motors': motors,
                    'service_types': service_types,
                    'post_data': request.POST,
                    'booking_type': booking_type,
                })
            
            # Create booking
            # update user's name/phone if provided
            if first_name:
                request.user.first_name = first_name
                request.user.save()

            booking = ServiceBooking.objects.create(
                booking_number=booking_number,
                motor=motor,
                customer=request.user,
                service_type=service_type,
                booking_type=booking_type,
                status='pending',
                complaint=complaint,
                booking_date=today,
            )
            
            messages.success(request, f'Booking berhasil! Nomor booking: {booking.booking_number}')
            return redirect('customer:customer_dashboard')
            
        except Exception as e:
            messages.error(request, f'Gagal membuat booking: {str(e)}')
    
    context = {
        'motors': motors,
        'service_types': service_types,
    }
    
    return render(request, 'customer/booking_create.html', context)

@customer_required
def service_history(request):
    """Daftar riwayat servis selesai"""
    # Get all bookings for this customer
    bookings = ServiceBooking.objects.filter(
        customer=request.user
    ).select_related('motor', 'service_type', 'mechanic').order_by('-booking_date')
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'status_choices': ServiceBooking.STATUS_CHOICES,
    }
    
    return render(request, 'customer/service_history.html', context)

@customer_required
def invoice_detail(request, pk):
    """Detail biaya dan nota servis"""
    booking = get_object_or_404(ServiceBooking, pk=pk, customer=request.user)
    
    # Try to get invoice
    try:
        invoice = Invoice.objects.get(service_booking=booking)
    except Invoice.DoesNotExist:
        invoice = None
    
    context = {
        'booking': booking,
        'invoice': invoice,
    }
    
    return render(request, 'customer/invoice_detail.html', context)
