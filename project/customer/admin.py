from django.contrib import admin
from .models import Motor, ServiceType, ServiceBooking, SparePart, AdditionalService, Invoice

# Register your models here.

@admin.register(Motor)
class MotorAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'brand', 'model', 'year', 'owner', 'created_at')
    list_filter = ('brand', 'year', 'created_at')
    search_fields = ('license_plate', 'brand', 'model', 'owner__username')
    ordering = ('-created_at',)

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'estimated_duration', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'motor', 'customer', 'service_type', 'mechanic', 'status', 'booking_date')
    list_filter = ('status', 'booking_type', 'booking_date')
    search_fields = ('booking_number', 'motor__license_plate', 'customer__username')
    ordering = ('-booking_date',)

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_booking', 'quantity', 'unit_price', 'total_price')
    search_fields = ('name', 'service_booking__booking_number')
    ordering = ('-created_at',)

@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_booking', 'price')
    search_fields = ('name', 'service_booking__booking_number')
    ordering = ('-created_at',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'service_booking', 'total_cost', 'payment_method', 'cashier', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('invoice_number', 'service_booking__booking_number')
    ordering = ('-created_at',)
