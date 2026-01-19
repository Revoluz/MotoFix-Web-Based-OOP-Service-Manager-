@echo off
REM MotoFix Django Project - Windows Setup Script
REM This script automates the setup process for Windows

echo ================================================
echo MotoFix - Windows Setup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed!
    echo Please reinstall Python with pip enabled.
    pause
    exit /b 1
)

echo [OK] pip is installed
echo.

REM Create virtual environment
echo [STEP 1/7] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created successfully
)
echo.

REM Activate virtual environment
echo [STEP 2/7] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo [STEP 3/7] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [STEP 4/7] Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo [OK] Dependencies installed successfully
echo.

REM Create .env file if it doesn't exist
echo [STEP 5/7] Setting up environment variables...
if exist .env (
    echo .env file already exists. Skipping creation.
) else (
    if exist .env.example (
        copy .env.example .env
        echo [OK] Created .env file from .env.example
    ) else (
        echo SECRET_KEY=django-insecure-change-this-in-production-@#$%%^^*()!> .env
        echo DEBUG=True>> .env
        echo ALLOWED_HOSTS=localhost,127.0.0.1>> .env
        echo [OK] Created default .env file
        echo [WARNING] Please update your SECRET_KEY in the .env file!
    )
)
echo.

REM Check if manage.py exists (Django project initialized)
if not exist manage.py (
    echo [STEP 6/7] Django project not found. Initializing...
    echo [INFO] You may need to create a Django project manually using:
    echo        django-admin startproject motofix .
    echo.
) else (
    echo [STEP 6/7] Running database migrations...
    python manage.py makemigrations
    python manage.py migrate
    if errorlevel 1 (
        echo [WARNING] Migration failed, but continuing...
    ) else (
        echo [OK] Migrations completed successfully
    )
    echo.
    
    echo [STEP 7/7] Creating demo users...
    python manage.py seed_users
    if errorlevel 1 (
        echo [WARNING] Failed to create demo users, but continuing...
    ) else (
        echo [OK] Demo users created successfully
    )
    echo.
)

echo Setup complete!
echo.
echo ================================================
echo Setup completed successfully!
echo ================================================
echo.
echo Next steps:
echo 1. Review and update the .env file with your settings
if exist manage.py (
    echo 2. Run the development server: python manage.py runserver
    echo 3. Visit http://127.0.0.1:8000/ in your browser
    echo 4. Login with demo credentials ^(see README.md^)
    echo.
    echo Demo credentials:
    echo    Admin:    admin / admin123
    echo    Kasir:    kasir / kasir123
    echo    Mekanik:  mekanik / mekanik123
    echo    Customer: customer / customer123
) else (
    echo 2. Initialize Django project: django-admin startproject motofix .
    echo 3. Create a superuser: python manage.py createsuperuser
    echo 4. Run the development server: python manage.py runserver
)
echo.
echo To activate virtual environment later, run: venv\Scripts\activate
echo To deactivate, run: deactivate
echo.
pause
