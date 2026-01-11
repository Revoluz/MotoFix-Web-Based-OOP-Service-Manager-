# Script untuk membuat data layanan demo
# Jalankan dengan: python manage.py shell < setup_demo_services.py

from customer.models import ServiceType

print("🔧 Membuat data jenis layanan demo...")
print("=" * 50)

# Hapus layanan lama jika ada
ServiceType.objects.all().delete()

# Data layanan
services_data = [
    {
        'name': 'Servis Berkala',
        'description': 'Servis rutin untuk pemeliharaan rutin motor',
        'base_price': 50000,
        'estimated_duration': 60,
    },
    {
        'name': 'Ganti Oli',
        'description': 'Penggantian oli mesin motor',
        'base_price': 35000,
        'estimated_duration': 30,
    },
    {
        'name': 'Ganti Filter Udara',
        'description': 'Penggantian filter udara motor',
        'base_price': 25000,
        'estimated_duration': 20,
    },
    {
        'name': 'Servis Rem',
        'description': 'Pemeriksaan dan perbaikan sistem rem',
        'base_price': 75000,
        'estimated_duration': 90,
    },
    {
        'name': 'Servis Rantai',
        'description': 'Pembersihan, pelumasan, dan pengaturan rantai motor',
        'base_price': 45000,
        'estimated_duration': 45,
    },
    {
        'name': 'Tuning Motor',
        'description': 'Optimalisasi performa motor',
        'base_price': 150000,
        'estimated_duration': 120,
    },
    {
        'name': 'Ganti Busi',
        'description': 'Penggantian busi dengan kualitas terbaik',
        'base_price': 30000,
        'estimated_duration': 20,
    },
    {
        'name': 'Servis Karburator',
        'description': 'Pembersihan dan penggantian suku cadang karburator',
        'base_price': 80000,
        'estimated_duration': 90,
    },
]

# Buat layanan
for service_data in services_data:
    service = ServiceType.objects.create(
        name=service_data['name'],
        description=service_data['description'],
        base_price=service_data['base_price'],
        estimated_duration=service_data['estimated_duration'],
        is_active=True
    )
    print(f"✓ {service.name} - Rp {service.base_price:,.0f}")

print("=" * 50)
print(f"✅ {len(services_data)} jenis layanan berhasil dibuat!")
