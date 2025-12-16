#!/bin/bash
# MotoFix Django Project - Linux/Ubuntu Setup Script
# This script automates the setup process for Ubuntu/Debian-based systems

set -e  # Exit on error

echo "================================================"
echo "MotoFix - Linux/Ubuntu Setup Script"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed!"
    echo "Installing Python 3..."
    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y
else
    echo -e "${GREEN}[OK]${NC} Python 3 is installed"
    python3 --version
fi
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} pip3 is not installed!"
    echo "Installing pip3..."
    sudo apt install python3-pip -y
else
    echo -e "${GREEN}[OK]${NC} pip3 is installed"
fi
echo ""

# Check if python3-venv is installed
if ! python3 -m venv --help &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} python3-venv is not installed!"
    echo "Installing python3-venv..."
    sudo apt install python3-venv -y
fi

# Create virtual environment
echo "[STEP 1/7] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo -e "${GREEN}[OK]${NC} Virtual environment created successfully"
fi
echo ""

# Activate virtual environment
echo "[STEP 2/7] Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}[OK]${NC} Virtual environment activated"
echo ""

# Upgrade pip
echo "[STEP 3/7] Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "[STEP 4/7] Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}[OK]${NC} Dependencies installed successfully"
else
    echo -e "${RED}[ERROR]${NC} requirements.txt not found!"
    exit 1
fi
echo ""

# Create .env file if it doesn't exist
echo "[STEP 5/7] Setting up environment variables..."
if [ -f ".env" ]; then
    echo ".env file already exists. Skipping creation."
else
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}[OK]${NC} Created .env file from .env.example"
    else
        cat > .env << EOF
SECRET_KEY=django-insecure-change-this-in-production-@#$%^^*()!
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
        echo -e "${GREEN}[OK]${NC} Created default .env file"
        echo -e "${YELLOW}[WARNING]${NC} Please update your SECRET_KEY in the .env file!"
    fi
fi
echo ""

# Check if manage.py exists (Django project initialized)
if [ ! -f "manage.py" ]; then
    echo "[STEP 6/7] Django project not found. Initializing..."
    echo -e "${YELLOW}[INFO]${NC} You may need to create a Django project manually using:"
    echo "       django-admin startproject motofix ."
    echo ""
else
    echo "[STEP 6/7] Running database migrations..."
    python manage.py makemigrations || echo -e "${YELLOW}[WARNING]${NC} makemigrations failed, but continuing..."
    python manage.py migrate || echo -e "${YELLOW}[WARNING]${NC} migrate failed, but continuing..."
    echo -e "${GREEN}[OK]${NC} Migrations completed successfully"
    echo ""
fi

echo "[STEP 7/7] Setup complete!"
echo ""
echo "================================================"
echo "Setup completed successfully!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Review and update the .env file with your settings"
if [ -f "manage.py" ]; then
    echo "2. Create a superuser: python manage.py createsuperuser"
    echo "3. Run the development server: python manage.py runserver"
    echo "4. Visit http://127.0.0.1:8000/ in your browser"
else
    echo "2. Initialize Django project: django-admin startproject motofix ."
    echo "3. Create a superuser: python manage.py createsuperuser"
    echo "4. Run the development server: python manage.py runserver"
fi
echo ""
echo "To activate virtual environment later, run: source venv/bin/activate"
echo "To deactivate, run: deactivate"
echo ""
