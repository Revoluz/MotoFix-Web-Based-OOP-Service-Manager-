# 🗄️ Setup Database MySQL untuk MotoFix

## Langkah 1: Install MySQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# Arch Linux
sudo pacman -S mysql
sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
sudo systemctl start mysqld
```

## Langkah 2: Login ke MySQL

```bash
sudo mysql -u root -p
```

## Langkah 3: Buat Database

```sql
-- Buat database
CREATE DATABASE motofix_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Buat user (optional, jika tidak ingin pakai root)
CREATE USER 'motofix_user'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON motofix_db.* TO 'motofix_user'@'localhost';
FLUSH PRIVILEGES;

-- Keluar
EXIT;
```

## Langkah 4: Install MySQL Driver untuk Python

```bash
# Aktifkan virtual environment
cd /home/fanxx/Coding/study/collage/oop/MotoFix-Web-Based-OOP-Service-Manager-
source venv/bin/activate

# Install mysqlclient
pip install mysqlclient
```

**Jika error saat install mysqlclient:**

```bash
# Ubuntu/Debian
sudo apt install python3-dev default-libmysqlclient-dev build-essential

# Arch Linux
sudo pacman -S mysql-clients
```

## Langkah 5: Update settings.py

File `project/motoService/settings.py` sudah dikonfigurasi dengan:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'motofix_db',
        'USER': 'root',
        'PASSWORD': '',  # Ganti dengan password MySQL Anda
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**⚠️ PENTING:** Ganti `PASSWORD` dengan password MySQL Anda!

## Langkah 6: Jalankan Migrasi

```bash
cd project

# Hapus migrasi lama (jika ada)
rm -rf accounts/migrations/__pycache__
rm -rf accounts/migrations/0*.py

# Buat migrasi baru
python manage.py makemigrations

# Terapkan migrasi
python manage.py migrate
```

## Langkah 7: Buat Superuser (Admin)

```bash
python manage.py createsuperuser
```

**Contoh input:**
- Username: `admin`
- Email: `admin@motofix.com`
- Password: `admin123`
- Password (again): `admin123`

## Langkah 8: Buat User Demo

```bash
python manage.py shell
```

Kemudian jalankan:

```python
from accounts.models import User

# Buat user customer
User.objects.create_user(
    username='customer',
    email='customer@test.com',
    password='customer123',
    role='customer',
    phone='08123456789',
    address='Jl. Test No. 123'
)

# Buat user mekanik
User.objects.create_user(
    username='mekanik',
    email='mekanik@test.com',
    password='mekanik123',
    role='mechanic',
    phone='08234567890'
)

# Buat user kasir
User.objects.create_user(
    username='kasir',
    email='kasir@test.com',
    password='kasir123',
    role='cashier'
)

# Keluar
exit()
```

## Langkah 9: Jalankan Server

```bash
python manage.py runserver
```

Buka browser: **http://127.0.0.1:8000/**

## 🎯 Testing Login

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Customer | customer | customer123 |
| Mekanik | mekanik | mekanik123 |
| Kasir | kasir | kasir123 |

## 📝 Troubleshooting

### Error: Can't connect to MySQL server

```bash
# Start MySQL service
sudo systemctl start mysql

# Check status
sudo systemctl status mysql
```

### Error: Access denied for user 'root'@'localhost'

```bash
# Reset MySQL root password
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
EXIT;
```

### Error: No module named 'MySQLdb'

```bash
pip install mysqlclient
```

Jika masih error, install dependencies:

```bash
# Ubuntu/Debian
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config

# Arch Linux
sudo pacman -S mariadb-libs
```
