# Script untuk membuat user demo
# Jalankan dengan: python manage.py shell < setup_demo_users.py

from accounts.models import User

print("🔧 Membuat user demo untuk MotoFix...")
print("=" * 50)

# Hapus user demo jika sudah ada
User.objects.filter(username__in=['customer', 'mekanik', 'kasir']).delete()

# Buat user customer
customer = User.objects.create_user(
    username='customer',
    email='customer@test.com',
    password='customer123',
    role='customer',
    phone='08123456789',
    address='Jl. Pelanggan No. 123, Jakarta'
)
print(f"✓ User Customer dibuat: {customer.username}")

# Buat user mekanik
mekanik = User.objects.create_user(
    username='mekanik',
    email='mekanik@test.com',
    password='mekanik123',
    role='mechanic',
    phone='08234567890',
    address='Jl. Mekanik No. 456, Jakarta'
)
print(f"✓ User Mekanik dibuat: {mekanik.username}")

# Buat user kasir
kasir = User.objects.create_user(
    username='kasir',
    email='kasir@test.com',
    password='kasir123',
    role='cashier',
    phone='08345678901',
    address='Jl. Kasir No. 789, Jakarta'
)
print(f"✓ User Kasir dibuat: {kasir.username}")

print("=" * 50)
print("✅ User demo berhasil dibuat!")
print("")
print("📋 Daftar User:")
print("-" * 50)
print("| Role     | Username | Password     |")
print("-" * 50)
print("| Customer | customer | customer123  |")
print("| Mekanik  | mekanik  | mekanik123   |")
print("| Kasir    | kasir    | kasir123     |")
print("-" * 50)
print("")
print("🚀 Jalankan server dengan: python manage.py runserver")
