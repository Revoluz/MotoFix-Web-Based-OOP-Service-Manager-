#!/bin/bash

# Script untuk setup database MySQL dan migrasi Django
# Untuk proyek MotoFix

echo "🗄️ Setup Database MySQL untuk MotoFix"
echo "======================================"
echo ""

# Warna
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fungsi untuk cek apakah command ada
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Simpan direktori awal (root project)
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# 1. Cek MySQL
echo -e "${YELLOW}[1/7]${NC} Mengecek MySQL..."
if ! command_exists mysql; then
    echo -e "${RED}❌ MySQL tidak terinstall!${NC}"
    echo "Install dengan: sudo apt install mysql-server (Ubuntu/Debian)"
    echo "Atau: sudo pacman -S mysql (Arch Linux)"
    exit 1
fi
echo -e "${GREEN}✓ MySQL terinstall${NC}"
echo ""

# 2. Cek Python
echo -e "${YELLOW}[2/7]${NC} Mengecek Python..."
if ! command_exists python3; then
    echo -e "${RED}❌ Python3 tidak terinstall!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 terinstall${NC}"
echo ""

# 3. Aktifkan virtual environment
echo -e "${YELLOW}[3/7]${NC} Mengaktifkan virtual environment..."
cd "$PROJECT_ROOT"
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment aktif${NC}"
else
    echo -e "${RED}❌ Virtual environment tidak ditemukan!${NC}"
    echo "Jalankan: python3 -m venv venv"
    exit 1
fi
echo ""

# 4. Install mysqlclient
echo -e "${YELLOW}[4/7]${NC} Menginstall mysqlclient..."
pip install mysqlclient > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ mysqlclient terinstall${NC}"
else
    echo -e "${RED}❌ Gagal install mysqlclient${NC}"
    echo "Install dependencies dulu:"
    echo "Ubuntu/Debian: sudo apt install python3-dev default-libmysqlclient-dev build-essential"
    echo "Arch Linux: sudo pacman -S mariadb-libs"
    exit 1
fi
echo ""

# 5. Input password MySQL
echo -e "${YELLOW}[5/7]${NC} Setup database MySQL..."
echo "Masukkan password MySQL root (tekan Enter jika tidak ada password):"
read -s MYSQL_PASSWORD
echo ""

# 6. Buat database
echo "Membuat database..."
if [ -z "$MYSQL_PASSWORD" ]; then
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS motofix_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null
    DB_CREATE=$?
else
    mysql -u root -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS motofix_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null
    DB_CREATE=$?
fi

if [ $DB_CREATE -eq 0 ]; then
    echo -e "${GREEN}✓ Database motofix_db berhasil dibuat${NC}"
else
    echo -e "${RED}❌ Gagal membuat database!${NC}"
    echo "Periksa username dan password MySQL Anda."
    exit 1
fi

# 7. Update settings.py dengan password
echo -e "${YELLOW}[6/7]${NC} Mengupdate konfigurasi database..."
SETTINGS_FILE="$PROJECT_ROOT/project/motoService/settings.py"

# Escape special characters untuk sed
ESCAPED_PASSWORD=$(echo "$MYSQL_PASSWORD" | sed 's/[\/&]/\\&/g')

# Update password di settings.py
sed -i "s/'PASSWORD': ''/'PASSWORD': '$ESCAPED_PASSWORD'/" "$SETTINGS_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Konfigurasi database updated${NC}"
else
    echo -e "${YELLOW}⚠ Gagal update otomatis. Edit manual di $SETTINGS_FILE${NC}"
fi
echo ""

# 8. Jalankan migrasi
echo -e "${YELLOW}[7/7]${NC} Menjalankan migrasi Django..."
cd "$PROJECT_ROOT/project"

# Hapus migrasi lama
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete 2>/dev/null
find . -path "*/migrations/__pycache__/*" -delete 2>/dev/null

# Buat migrasi baru
echo "Membuat migrasi..."
python manage.py makemigrations

# Terapkan migrasi
echo "Menerapkan migrasi..."
python manage.py migrate

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Migrasi berhasil${NC}"
else
    echo -e "${RED}❌ Migrasi gagal${NC}"
    echo "Coba jalankan manual:"
    echo "  cd project"
    echo "  python manage.py migrate"
    exit 1
fi
echo ""

# Selesai
echo "======================================"
echo -e "${GREEN}✅ Setup database selesai!${NC}"
echo ""
echo "Langkah selanjutnya:"
echo "1. Buat superuser: python manage.py createsuperuser"
echo "2. Jalankan server: python manage.py runserver"
echo ""
echo "Atau jalankan script setup user demo:"
echo "  cd project && python manage.py shell < ../setup_demo_users.py"
echo ""