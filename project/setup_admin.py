# Script untuk membuat superuser admin
# Jalankan dengan: python manage.py shell < setup_admin.py

from accounts.models import User

print("🔧 Membuat superuser admin untuk MotoFix...")
print("=" * 50)

# Hapus admin jika sudah ada
User.objects.filter(username='admin').delete()

# Buat superuser admin
admin = User.objects.create_superuser(
    username='admin',
    email='admin@motofix.com',
    password='admin123',
    role='admin'
)
print(f"✓ Superuser Admin dibuat: {admin.username}")

print("=" * 50)
print("✅ Superuser berhasil dibuat!")
print("")
print("📋 Admin Login:")
print("-" * 50)
print("| Username | Password  |")
print("-" * 50)
print("| admin    | admin123  |")
print("-" * 50)
print("")
print("🚀 Login di: http://127.0.0.1:8000/accounts/login/")
print("🔐 Admin Panel: http://127.0.0.1:8000/admin/")
