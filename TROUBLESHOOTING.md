# Troubleshooting Guide

This guide helps you resolve common issues when setting up MotoFix on Windows or Linux.

## Table of Contents
- [Windows Issues](#windows-issues)
- [Linux Issues](#linux-issues)
- [Common Django Issues](#common-django-issues)
- [Database Issues](#database-issues)
- [Virtual Environment Issues](#virtual-environment-issues)

---

## Windows Issues

### Python is not recognized as internal or external command

**Cause:** Python is not in the system PATH

**Solutions:**
1. Reinstall Python and check "Add Python to PATH" during installation
2. Manually add Python to PATH:
   - Open System Properties → Advanced → Environment Variables
   - Add Python installation path (e.g., `C:\Python312\`) to PATH
   - Add Scripts folder (e.g., `C:\Python312\Scripts\`) to PATH
   - Restart Command Prompt

### Cannot activate virtual environment - Execution Policy Error

**Error:** `cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or use Command Prompt instead of PowerShell.

### pip install fails with "Access Denied"

**Solution:**
1. Run Command Prompt as Administrator
2. Or install in virtual environment (recommended)
3. Or use: `pip install --user -r requirements.txt`

### Module not found after installation

**Solution:**
```cmd
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### psycopg2 installation fails on Windows

**Solution:**
```cmd
# Use binary version instead
pip install psycopg2-binary

# Or if still failing, you can use SQLite instead (no need for psycopg2)
# Comment out psycopg2-binary in requirements.txt
```

---

## Linux Issues

### python3-venv is not available

**Error:** `The virtual environment was not created successfully`

**Solution:**
```bash
sudo apt update
sudo apt install python3-venv -y
```

### Permission denied errors

**Solutions:**

1. **For system-wide installations:**
```bash
sudo apt install python3-pip python3-venv
```

2. **For project files:**
```bash
# Fix ownership of project directory
sudo chown -R $USER:$USER /path/to/project

# Or ensure you're working in your home directory
```

3. **For virtual environment:**
```bash
# Don't use sudo with virtual environment commands
python3 -m venv venv  # Without sudo
source venv/bin/activate
pip install -r requirements.txt  # Without sudo
```

### pip command not found after activation

**Solution:**
```bash
# Use pip3 or python -m pip
python -m pip install -r requirements.txt

# Or upgrade pip
python -m pip install --upgrade pip
```

### libpq-dev missing (PostgreSQL issues)

**Error:** `Error: pg_config executable not found`

**Solution:**
```bash
sudo apt install libpq-dev python3-dev
pip install psycopg2-binary
```

### Pillow installation fails - missing dependencies

**Solution:**
```bash
sudo apt install libjpeg-dev zlib1g-dev libpng-dev
pip install Pillow
```

---

## Common Django Issues

### SECRET_KEY not set

**Error:** `django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty`

**Solution:**
```bash
# Create .env file
cp .env.example .env

# Or generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Add to .env file:
# SECRET_KEY=generated-key-here
```

### Port 8000 already in use

**Error:** `Error: That port is already in use`

**Solutions:**

1. **Use a different port:**
```bash
python manage.py runserver 8080
```

2. **Kill the process using port 8000:**

Windows:
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Linux:
```bash
lsof -ti:8000 | xargs kill -9
# or
sudo fuser -k 8000/tcp
```

### Migration errors

**Error:** `No such table` or migration conflicts

**Solutions:**

1. **Reset migrations (development only):**
```bash
# Delete SQLite database
rm db.sqlite3

# Delete migration files (keep __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

2. **Fake migrations:**
```bash
python manage.py migrate --fake-initial
```

### ALLOWED_HOSTS error

**Error:** `Invalid HTTP_HOST header`

**Solution:**
```python
# In .env file, add your host
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Or in settings.py for development only:
ALLOWED_HOSTS = ['*']  # NOT recommended for production
```

---

## Database Issues

### SQLite database is locked

**Solutions:**
1. Close all connections to the database
2. Restart the development server
3. Delete `db.sqlite3` and re-run migrations (development only)

### PostgreSQL connection refused

**Solutions:**

1. **Ensure PostgreSQL is running:**

Windows:
```cmd
# Check service
sc query postgresql

# Start service
net start postgresql
```

Linux:
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

2. **Check connection settings in .env:**
```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=motofix_db
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
```

3. **Create database if it doesn't exist:**
```bash
# Linux
sudo -u postgres psql
CREATE DATABASE motofix_db;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE motofix_db TO your_username;
\q
```

---

## Virtual Environment Issues

### Virtual environment not activating

**Windows:**
```cmd
# Use full path
C:\path\to\project\venv\Scripts\activate.bat

# Or change directory first
cd C:\path\to\project
venv\Scripts\activate
```

**Linux:**
```bash
# Use full path
source /path/to/project/venv/bin/activate

# Or change directory first
cd /path/to/project
source venv/bin/activate
```

### Wrong Python version in virtual environment

**Solution:**
```bash
# Create venv with specific Python version
python3.10 -m venv venv  # Linux
py -3.10 -m venv venv    # Windows

# Or recreate the virtual environment
rm -rf venv  # Linux
rmdir /s venv  # Windows
python -m venv venv
```

### Packages not found even after installation

**Solution:**
```bash
# Verify you're in the virtual environment
which python  # Linux
where python  # Windows

# Should point to venv directory
# If not, reactivate:
deactivate
source venv/bin/activate  # Linux
venv\Scripts\activate  # Windows
```

---

## Performance Issues

### Slow pip install

**Solutions:**
1. **Upgrade pip:**
```bash
pip install --upgrade pip
```

2. **Use binary packages when available:**
```bash
pip install --only-binary :all: -r requirements.txt
```

3. **Clear pip cache:**
```bash
pip cache purge
```

### Development server is slow

**Solutions:**
1. Ensure DEBUG=True is only used in development
2. Use SQLite for development, PostgreSQL for production
3. Disable django-debug-toolbar in production

---

## Getting Help

If you're still experiencing issues:

1. **Check Django logs:**
   - Look for error messages in the console
   - Check `debug.log` if logging is configured

2. **Verify your setup:**
```bash
python manage.py check
python manage.py check --deploy  # Production checklist
```

3. **Create an issue:**
   - Include your OS and Python version
   - Include the full error message
   - Include steps to reproduce the problem

4. **Useful commands for debugging:**
```bash
# Check Python version
python --version

# Check Django version
python -m django --version

# List installed packages
pip list

# Verify virtual environment
which python  # Linux
where python  # Windows

# Check Django configuration
python manage.py diffsettings
```

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
