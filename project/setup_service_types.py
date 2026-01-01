#!/usr/bin/env python
"""
Script untuk membuat demo service types
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motoService.settings')
django.setup()

from customer.models import ServiceType

def create_service_types():
    """Membuat demo service types"""
    
    service_types = [
        {
            'name': 'Servis Rutin',
            'description': 'Servis berkala meliputi ganti oli, cek rem, dan tune up dasar',
            'base_price': 150000,
            'estimated_duration': 60,
        },
        {
            'name': 'Ganti Oli',
            'description': 'Penggantian oli mesin dengan oli berkualitas',
            'base_price': 75000,
            'estimated_duration': 30,
        },
        {
            'name': 'Tune Up',
            'description': 'Tune up lengkap untuk performa optimal',
            'base_price': 200000,
            'estimated_duration': 90,
        },
        {
            'name': 'Ganti Ban',
            'description': 'Penggantian ban motor (belum termasuk harga ban)',
            'base_price': 50000,
            'estimated_duration': 45,
        },
        {
            'name': 'Servis Rem',
            'description': 'Perawatan dan perbaikan sistem pengereman',
            'base_price': 100000,
            'estimated_duration': 60,
        },
        {
            'name': 'Servis Mesin',
            'description': 'Perbaikan dan perawatan mesin motor',
            'base_price': 350000,
            'estimated_duration': 180,
        },
        {
            'name': 'Ganti Kampas Rem',
            'description': 'Penggantian kampas rem depan/belakang',
            'base_price': 120000,
            'estimated_duration': 45,
        },
        {
            'name': 'Cuci Motor',
            'description': 'Pencucian motor dengan shampoo khusus dan semir ban',
            'base_price': 25000,
            'estimated_duration': 20,
        },
    ]
    
    created_count = 0
    for service_data in service_types:
        service, created = ServiceType.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        if created:
            created_count += 1
            print(f"✓ Created: {service.name} - Rp {service.base_price:,.0f}")
        else:
            print(f"- Already exists: {service.name}")
    
    print(f"\n✅ Selesai! {created_count} service types baru dibuat.")
    print(f"📊 Total service types: {ServiceType.objects.count()}")

if __name__ == '__main__':
    print("🔧 Membuat demo service types...\n")
    create_service_types()
