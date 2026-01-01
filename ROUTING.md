# 🛣️ Dokumentasi Routing MotoFix

## Struktur Folder Django

```
project/
├── manage.py
├── db.sqlite3
├── motoService/              # Project settings
│   ├── __init__.py
│   ├── settings.py          # Konfigurasi utama
│   ├── urls.py              # URL routing utama
│   ├── views.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                 # App untuk autentikasi
│   ├── views.py
│   ├── urls.py
│   └── ...
├── customer/                 # App untuk panel pelanggan
│   ├── views.py
│   ├── urls.py
│   └── ...
├── admin_hub/               # App untuk panel admin
│   ├── views.py
│   ├── urls.py
│   └── ...
└── templates/               # HTML templates
    ├── base.html           # Base template
    ├── accounts/
    │   ├── login.html
    │   └── register.html
    ├── customer/
    │   ├── dashboard.html
    │   ├── motor_add.html
    │   ├── motor_edit.html
    │   ├── booking_create.html
    │   ├── service_history.html
    │   └── invoice_detail.html
    └── admin_hub/
        ├── dashboard.html
        ├── allocate_mechanic.html
        ├── service_start.html
        ├── service_update.html
        ├── service_finish.html
        ├── process_payment.html
        ├── service_list.html
        ├── service_add.html
        └── mechanic_list.html
```

## Daftar Routes URL

### 1️⃣ Autentikasi & Akun (`accounts/`)

| URL Path | Name | View | Template | Deskripsi |
|----------|------|------|----------|-----------|
| `accounts/login/` | `login` | `accounts.views.login` | `accounts/login.html` | Halaman login untuk semua user |
| `accounts/logout/` | `logout` | `accounts.views.logout` | - | Proses logout |
| `accounts/register/` | `register` | `accounts.views.register` | `accounts/register.html` | Halaman pendaftaran pelanggan baru |

### 2️⃣ Panel Pelanggan (`customer/`)

| URL Path | Name | View | Template | Deskripsi |
|----------|------|------|----------|-----------|
| `customer/dashboard/` | `customer_dashboard` | `customer.views.customer_dashboard` | `customer/dashboard.html` | Dashboard utama & tracking status aktif |
| `customer/motor/add/` | `motor_add` | `customer.views.motor_add` | `customer/motor_add.html` | Form tambah motor baru |
| `customer/motor/<int:pk>/edit/` | `motor_edit` | `customer.views.motor_edit` | `customer/motor_edit.html` | Form edit data motor |
| `customer/booking/` | `booking_create` | `customer.views.booking_create` | `customer/booking_create.html` | Form buat antrian (Booking/Walk-in) |
| `customer/history/` | `service_history` | `customer.views.service_history` | `customer/service_history.html` | Daftar riwayat servis selesai |
| `customer/invoice/<int:pk>/` | `invoice_detail` | `customer.views.invoice_detail` | `customer/invoice_detail.html` | Detail biaya dan nota servis |

### 3️⃣ Panel Admin & Manajemen (`admin-hub/`)

#### Dashboard
| URL Path | Name | View | Template | Deskripsi |
|----------|------|------|----------|-----------|
| `admin-hub/dashboard/` | `admin_dashboard` | `admin_hub.views.admin_dashboard` | `admin_hub/dashboard.html` | Monitoring seluruh antrian & status bengkel |

#### Manajemen Tugas
| URL Path | Name | View | Template | Deskripsi |
|----------|------|------|----------|-----------|
| `admin-hub/queue/<int:pk>/allocate/` | `allocate_mechanic` | `admin_hub.views.allocate_mechanic` | `admin_hub/allocate_mechanic.html` | Proses admin menugaskan mekanik |
| `admin-hub/service/<int:pk>/start/` | `service_start` | `admin_hub.views.service_start` | `admin_hub/service_start.html` | Trigger mekanik mulai bekerja (via Admin) |
| `admin-hub/service/<int:pk>/update/` | `service_update` | `admin_hub.views.service_update` | `admin_hub/service_update.html` | Input suku cadang & jasa tambahan (Modal) |
| `admin-hub/service/<int:pk>/finish/` | `service_finish` | `admin_hub.views.service_finish` | `admin_hub/service_finish.html` | Menandai pengerjaan mekanik selesai |

#### Kasir & Pembayaran
| URL Path | Name | View | Template | Deskripsi |
|----------|------|------|----------|-----------|
| `admin-hub/payment/<int:pk>/` | `process_payment` | `admin_hub.views.process_payment` | `admin_hub/process_payment.html` | Form kasir untuk konfirmasi pembayaran |

#### Master Data
| URL Path | Name | View | Template | Deskripsi |
|----------|------|------|----------|-----------|
| `admin-hub/services/` | `service_list` | `admin_hub.views.service_list` | `admin_hub/service_list.html` | List semua jenis layanan (Master Data) |
| `admin-hub/services/add/` | `service_add` | `admin_hub.views.service_add` | `admin_hub/service_add.html` | Form tambah jenis layanan baru |
| `admin-hub/mechanics/` | `mechanic_list` | `admin_hub.views.mechanic_list` | `admin_hub/mechanic_list.html` | List data mekanik |

## Cara Menggunakan URL dengan Namespace

Dalam template HTML, gunakan `{% url %}` tag dengan namespace:

```django
<!-- Contoh di template -->
<a href="{% url 'accounts:login' %}">Login</a>
<a href="{% url 'customer:customer_dashboard' %}">Dashboard</a>
<a href="{% url 'admin_hub:admin_dashboard' %}">Admin Hub</a>

<!-- Dengan parameter -->
<a href="{% url 'customer:motor_edit' pk=1 %}">Edit Motor</a>
<a href="{% url 'customer:invoice_detail' pk=5 %}">Lihat Invoice</a>
```

Dalam views Python, gunakan `reverse()`:

```python
from django.urls import reverse
from django.shortcuts import redirect

# Redirect ke halaman lain
return redirect('accounts:login')
return redirect('customer:customer_dashboard')

# Dengan parameter
return redirect('customer:motor_edit', pk=motor_id)
```

## Cara Menjalankan Server

```bash
# Aktifkan virtual environment
cd /home/fanxx/Coding/study/collage/oop/MotoFix-Web-Based-OOP-Service-Manager-
source venv/bin/activate

# Masuk ke folder project
cd project

# Jalankan server
python manage.py runserver
```

Server akan berjalan di: **http://127.0.0.1:8000/**

## URL yang Bisa Diakses

- Homepage: http://127.0.0.1:8000/ (redirect ke login)
- Login: http://127.0.0.1:8000/accounts/login/
- Register: http://127.0.0.1:8000/accounts/register/
- Customer Dashboard: http://127.0.0.1:8000/customer/dashboard/
- Admin Dashboard: http://127.0.0.1:8000/admin-hub/dashboard/
- Django Admin: http://127.0.0.1:8000/admin/
