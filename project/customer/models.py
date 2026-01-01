from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Motor(models.Model):
    """
    Model untuk data motor pelanggan
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='motors')
    license_plate = models.CharField(max_length=15, unique=True, verbose_name='Plat Nomor')
    brand = models.CharField(max_length=50, verbose_name='Merk')
    model = models.CharField(max_length=50, verbose_name='Model/Tipe')
    year = models.IntegerField(verbose_name='Tahun')
    # color = models.CharField(max_length=30, verbose_name='Warna')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'motors'
        verbose_name = 'Motor'
        verbose_name_plural = 'Motor'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.license_plate} - {self.brand} {self.model} ({self.owner.username})"


class ServiceType(models.Model):
    """
    Model untuk jenis layanan servis (Master Data)
    """
    name = models.CharField(max_length=100, verbose_name='Nama Layanan')
    description = models.TextField(blank=True, null=True, verbose_name='Deskripsi')
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Harga Dasar')
    estimated_duration = models.IntegerField(help_text='Durasi estimasi dalam menit', verbose_name='Estimasi Durasi (menit)')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_types'
        verbose_name = 'Jenis Layanan'
        verbose_name_plural = 'Jenis Layanan'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - Rp {self.base_price:,.0f}"


class ServiceBooking(models.Model):
    """
    Model untuk antrian/booking servis
    """
    STATUS_CHOICES = (
        ('pending', 'Menunggu'),
        ('assigned', 'Ditugaskan ke Mekanik'),
        ('in_progress', 'Sedang Dikerjakan'),
        ('finished', 'Selesai Dikerjakan'),
        ('paid', 'Sudah Dibayar'),
        ('cancelled', 'Dibatalkan'),
    )
    
    BOOKING_TYPE_CHOICES = (
        ('booking', 'Booking Online'),
        ('walk_in', 'Walk-in'),
    )
    
    booking_number = models.CharField(max_length=20, unique=True, verbose_name='Nomor Booking')
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, related_name='bookings')
    mechanic = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_services',
        limit_choices_to={'role': 'mechanic'}
    )
    
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPE_CHOICES, default='booking')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    complaint = models.TextField(verbose_name='Keluhan/Permintaan')
    notes = models.TextField(blank=True, null=True, verbose_name='Catatan Tambahan')
    
    # Timestamps
    booking_date = models.DateTimeField(default=timezone.now, verbose_name='Tanggal Booking')
    assigned_date = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Ditugaskan')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Mulai')
    finish_date = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Selesai')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Pembayaran')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_bookings'
        verbose_name = 'Booking Servis'
        verbose_name_plural = 'Booking Servis'
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"{self.booking_number} - {self.motor.license_plate} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        if not self.booking_number:
            # Generate booking number: BK-YYYYMMDD-XXXX
            from django.utils import timezone
            today = timezone.now().strftime('%Y%m%d')
            last_booking = ServiceBooking.objects.filter(
                booking_number__startswith=f'BK-{today}'
            ).order_by('-booking_number').first()
            
            if last_booking:
                last_num = int(last_booking.booking_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.booking_number = f'BK-{today}-{new_num:04d}'
        
        super().save(*args, **kwargs)


class SparePart(models.Model):
    """
    Model untuk suku cadang yang digunakan dalam servis
    """
    service_booking = models.ForeignKey(ServiceBooking, on_delete=models.CASCADE, related_name='spare_parts')
    name = models.CharField(max_length=100, verbose_name='Nama Suku Cadang')
    quantity = models.IntegerField(default=1, verbose_name='Jumlah')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Harga Satuan')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Harga')
    notes = models.TextField(blank=True, null=True, verbose_name='Catatan')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'spare_parts'
        verbose_name = 'Suku Cadang'
        verbose_name_plural = 'Suku Cadang'
    
    def __str__(self):
        return f"{self.name} x{self.quantity} - Rp {self.total_price:,.0f}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class AdditionalService(models.Model):
    """
    Model untuk jasa tambahan dalam servis
    """
    service_booking = models.ForeignKey(ServiceBooking, on_delete=models.CASCADE, related_name='additional_services')
    name = models.CharField(max_length=100, verbose_name='Nama Jasa')
    description = models.TextField(blank=True, null=True, verbose_name='Deskripsi')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Harga')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'additional_services'
        verbose_name = 'Jasa Tambahan'
        verbose_name_plural = 'Jasa Tambahan'
    
    def __str__(self):
        return f"{self.name} - Rp {self.price:,.0f}"


class Invoice(models.Model):
    """
    Model untuk invoice/nota pembayaran
    """
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Tunai'),
        ('debit', 'Kartu Debit'),
        ('credit', 'Kartu Kredit'),
        ('transfer', 'Transfer Bank'),
        ('ewallet', 'E-Wallet'),
    )
    
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name='Nomor Invoice')
    service_booking = models.OneToOneField(ServiceBooking, on_delete=models.CASCADE, related_name='invoice')
    
    # Biaya
    service_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Biaya Servis')
    spare_parts_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Biaya Suku Cadang')
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Biaya Tambahan')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Biaya')
    
    # Pembayaran
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Metode Pembayaran')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Jumlah Dibayar')
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Kembalian')
    
    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='processed_invoices',
        limit_choices_to={'role': 'cashier'}
    )
    
    notes = models.TextField(blank=True, null=True, verbose_name='Catatan')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoice'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.invoice_number} - Rp {self.total_cost:,.0f}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number: INV-YYYYMMDD-XXXX
            from django.utils import timezone
            today = timezone.now().strftime('%Y%m%d')
            last_invoice = Invoice.objects.filter(
                invoice_number__startswith=f'INV-{today}'
            ).order_by('-invoice_number').first()
            
            if last_invoice:
                last_num = int(last_invoice.invoice_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.invoice_number = f'INV-{today}-{new_num:04d}'
        
        # Calculate total
        self.total_cost = self.service_cost + self.spare_parts_cost + self.additional_cost
        self.change_amount = self.paid_amount - self.total_cost
        
        super().save(*args, **kwargs)
