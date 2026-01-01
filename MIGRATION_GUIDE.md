# 🔄 Panduan Migrasi Database Django - MotoFix

Panduan lengkap untuk mengelola migrasi database di proyek MotoFix.

---

## 📋 Daftar Isi

1. [Migrasi Dasar](#migrasi-dasar)
2. [Rollback Migrasi](#rollback-migrasi)
3. [Reset Database](#reset-database)
4. [Troubleshooting](#troubleshooting)
5. [Best Practices](#best-practices)

---

## 🚀 Migrasi Dasar

### 1. Setup Awal

```bash
# Masuk ke folder project
cd /home/fanxx/Coding/study/collage/oop/MotoFix-Web-Based-OOP-Service-Manager-/project

# Aktifkan virtual environment
source ../venv/bin/activate
```

### 2. Membuat File Migrasi

```bash
# Buat migrasi untuk semua apps
python manage.py makemigrations

# Buat migrasi untuk app tertentu
python manage.py makemigrations accounts

# Buat migrasi dengan nama custom
python manage.py makemigrations accounts --name add_user_profile
```

### 3. Menjalankan Migrasi

```bash
# Jalankan semua migrasi yang belum diterapkan
python manage.py migrate

# Jalankan migrasi untuk app tertentu
python manage.py migrate accounts

# Jalankan migrasi tertentu
python manage.py migrate accounts 0001
```

### 4. Melihat Status Migrasi

```bash
# Lihat semua migrasi
python manage.py showmigrations

# Lihat migrasi app tertentu
python manage.py showmigrations accounts

# Output:
# accounts
#  [X] 0001_initial        <- Sudah dijalankan
#  [ ] 0002_add_field      <- Belum dijalankan
```

---

## ⏮️ Rollback Migrasi

### 1. Rollback ke Migrasi Sebelumnya

```bash
# Lihat daftar migrasi
python manage.py showmigrations accounts

# Rollback ke migrasi tertentu (contoh: kembali ke 0001)
python manage.py migrate accounts 0001
```

### 2. Rollback ke State Awal (Zero)

```bash
# Rollback app accounts ke kondisi awal (sebelum migrasi)
python manage.py migrate accounts zero

# Ini akan membatalkan SEMUA migrasi di app accounts
```

### 3. Rollback Semua Apps

```bash
# Rollback semua apps ke zero
python manage.py migrate --fake accounts zero
python manage.py migrate --fake customer zero
python manage.py migrate --fake admin_hub zero
```

---

## 🔄 Reset Database

### Opsi 1: Reset Lengkap (Hapus DB & Mulai dari Awal)

```bash
# 1. Masuk ke MySQL
mysql -u root -p

# 2. Hapus dan buat ulang database
DROP DATABASE motofix_db;
CREATE DATABASE motofix_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 3. Hapus semua file migrasi
cd /home/fanxx/Coding/study/collage/oop/MotoFix-Web-Based-OOP-Service-Manager-/project
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/__pycache__/*" -delete

# 4. Buat migrasi baru
python manage.py makemigrations

# 5. Jalankan migrasi
python manage.py migrate

# 6. Buat superuser
python manage.py createsuperuser
```

### Opsi 2: Reset dengan Fake (Tandai Sudah Migrasi)

```bash
# 1. Rollback ke zero
python manage.py migrate accounts zero

# 2. Tandai sebagai sudah migrasi tanpa eksekusi SQL
python manage.py migrate --fake-initial
```

### Opsi 3: Reset Satu App Saja

```bash
# 1. Rollback app tertentu
python manage.py migrate accounts zero

# 2. Hapus file migrasi app tersebut
rm accounts/migrations/0*.py
rm -rf accounts/migrations/__pycache__

# 3. Buat migrasi baru
python manage.py makemigrations accounts

# 4. Jalankan migrasi
python manage.py migrate accounts
```

---

## 🔍 Perintah Useful Lainnya

### Melihat SQL yang Akan Dijalankan

```bash
# Lihat SQL dari migrasi tertentu
python manage.py sqlmigrate accounts 0001

# Output akan menampilkan query SQL yang akan dieksekusi
```

### Cek Masalah Migrasi

```bash
# Cek apakah ada perubahan model yang belum di-migrate
python manage.py makemigrations --check

# Cek apakah ada konflik migrasi
python manage.py makemigrations --dry-run
```

### Fake Migration (Tanpa Eksekusi)

```bash
# Tandai migrasi sebagai sudah dijalankan tanpa eksekusi SQL
python manage.py migrate --fake

# Berguna jika Anda sudah membuat tabel manual di database
python manage.py migrate accounts --fake
```

### Merge Migrasi yang Konflik

```bash
# Jika ada konflik migrasi (2 developer buat migrasi berbeda)
python manage.py makemigrations --merge
```

---

## 🐛 Troubleshooting

### Error: "No such table"

**Penyebab:** Migrasi belum dijalankan

**Solusi:**
```bash
python manage.py migrate
```

### Error: "Table already exists"

**Penyebab:** Tabel sudah ada di database tapi migrasi belum tercatat

**Solusi:**
```bash
# Tandai migrasi sebagai sudah dijalankan
python manage.py migrate --fake-initial
```

### Error: "Conflicting migrations detected"

**Penyebab:** Ada 2 migrasi dengan nomor yang sama

**Solusi:**
```bash
# Merge migrasi
python manage.py makemigrations --merge

# Atau hapus salah satu migrasi dan buat ulang
rm accounts/migrations/0002_*.py
python manage.py makemigrations
```

### Error: "Migration is not applied"

**Penyebab:** Migrasi sebelumnya belum dijalankan

**Solusi:**
```bash
# Jalankan semua migrasi yang tertunda
python manage.py migrate
```

### Error: "Access denied for user"

**Penyebab:** Password database salah di settings.py

**Solusi:**
```bash
# Edit project/motoService/settings.py
# Update PASSWORD di DATABASES configuration
```

### Reset Migrasi yang Rusak

```bash
# 1. Backup database
mysqldump -u root -p motofix_db > backup.sql

# 2. Hapus tabel django_migrations
mysql -u root -p
USE motofix_db;
DELETE FROM django_migrations WHERE app='accounts';
EXIT;

# 3. Fake migrate ulang
python manage.py migrate accounts --fake
```

---

## ✅ Best Practices

### 1. Sebelum Membuat Migrasi

```bash
# Selalu cek status migrasi terlebih dahulu
python manage.py showmigrations

# Pastikan tidak ada migrasi yang tertunda
python manage.py migrate
```

### 2. Penamaan Migrasi

```bash
# Gunakan nama yang deskriptif
python manage.py makemigrations --name add_user_role
python manage.py makemigrations --name remove_old_fields
```

### 3. Testing Migrasi

```bash
# Test di development dulu
python manage.py migrate --plan

# Lihat SQL yang akan dijalankan
python manage.py sqlmigrate accounts 0001
```

### 4. Backup Database

```bash
# Selalu backup sebelum migrasi penting
mysqldump -u root -p motofix_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore jika ada masalah
mysql -u root -p motofix_db < backup_20231218_120000.sql
```

### 5. Squashing Migrations (Gabungkan Banyak Migrasi)

```bash
# Jika sudah ada banyak migrasi, gabungkan menjadi satu
python manage.py squashmigrations accounts 0001 0010

# Ini akan membuat satu file migrasi yang menggabungkan 0001-0010
```

---

## 📊 Workflow Migrasi Standar

### Development

```bash
# 1. Edit models.py
nano accounts/models.py

# 2. Buat migrasi
python manage.py makemigrations

# 3. Review file migrasi yang dibuat
cat accounts/migrations/0002_*.py

# 4. Jalankan migrasi
python manage.py migrate

# 5. Test aplikasi
python manage.py runserver
```

### Production

```bash
# 1. Backup database
mysqldump -u root -p motofix_db > backup.sql

# 2. Pull kode terbaru
git pull origin main

# 3. Aktifkan virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Jalankan migrasi
python manage.py migrate

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Restart server
systemctl restart gunicorn
```

---

## 🎯 Quick Reference

| Perintah | Deskripsi |
|----------|-----------|
| `makemigrations` | Buat file migrasi dari perubahan models |
| `migrate` | Jalankan migrasi ke database |
| `showmigrations` | Lihat status semua migrasi |
| `sqlmigrate` | Lihat SQL dari migrasi tertentu |
| `migrate --fake` | Tandai migrasi sudah dijalankan tanpa eksekusi |
| `migrate app zero` | Rollback semua migrasi di app tertentu |
| `migrate app 0001` | Rollback ke migrasi tertentu |
| `makemigrations --merge` | Merge migrasi yang konflik |
| `squashmigrations` | Gabungkan beberapa migrasi jadi satu |

---

## 📞 Support

Jika mengalami masalah:

1. Cek file `TROUBLESHOOTING.md`
2. Lihat logs: `python manage.py migrate --verbosity 3`
3. Cek dokumentasi Django: https://docs.djangoproject.com/en/4.2/topics/migrations/

---

**Last Updated:** December 18, 2025  
**Project:** MotoFix - Web Based OOP Service Manager
