# Quick Start Guide

Get MotoFix up and running in 5 minutes!

## Prerequisites Check

Before you begin, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ pip (Python package manager) installed
- ✅ Git installed
- ✅ 10 minutes of your time

---

## Quick Setup (Automated)

### Windows

1. **Clone the repository:**
   ```cmd
   git clone https://github.com/Revoluz/MotoFix-Web-Based-OOP-Service-Manager-.git
   cd MotoFix-Web-Based-OOP-Service-Manager-
   ```

2. **Run the setup script:**
   ```cmd
   setup_windows.bat
   ```

3. **Create a superuser:**
   ```cmd
   venv\Scripts\activate
   python manage.py createsuperuser
   ```

4. **Start the server:**
   ```cmd
   python manage.py runserver
   ```

5. **Open your browser:**
   Navigate to `http://127.0.0.1:8000/`

### Linux/Ubuntu

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Revoluz/MotoFix-Web-Based-OOP-Service-Manager-.git
   cd MotoFix-Web-Based-OOP-Service-Manager-
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup_ubuntu.sh
   ./setup_ubuntu.sh
   ```

3. **Create a superuser:**
   ```bash
   source venv/bin/activate
   python manage.py createsuperuser
   ```

4. **Start the server:**
   ```bash
   python manage.py runserver
   ```

5. **Open your browser:**
   Navigate to `http://127.0.0.1:8000/`

---

## Manual Setup (3 Steps)

If automated setup doesn't work, here's the manual process:

### Step 1: Setup Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root:
```bash
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 3: Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## What's Next?

After setup is complete:

1. **Access the admin panel:**
   - Go to `http://127.0.0.1:8000/admin/`
   - Login with your superuser credentials

2. **Explore the application:**
   - Create your first ticket
   - Generate an invoice
   - Manage vehicles and services

3. **Customize settings:**
   - Edit `.env` file for environment-specific settings
   - Check `SETUP.md` for advanced configuration

---

## Common Commands

### Daily Development

```bash
# Activate virtual environment
source venv/bin/activate          # Linux
venv\Scripts\activate              # Windows

# Start development server
python manage.py runserver

# Create new app
python manage.py startapp myapp

# Make migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Useful Django Commands

```bash
# Open Django shell
python manage.py shell

# Run tests
python manage.py test

# Check for issues
python manage.py check

# View all available commands
python manage.py help
```

---

## Project Structure Overview

```
MotoFix/
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── .env                   # Environment vars (you create this)
├── venv/                  # Virtual environment
├── motofix/               # Main project
│   ├── settings.py        # Settings
│   └── urls.py            # URL routing
└── apps/                  # Your Django apps
    ├── tickets/           # Ticketing system
    ├── invoices/          # Invoice management
    └── ...
```

---

## Troubleshooting

### Issue: Command not found

**Solution:**
- Windows: Ensure Python is in PATH
- Linux: Use `python3` instead of `python`

### Issue: Port already in use

**Solution:**
```bash
# Use different port
python manage.py runserver 8080

# Or kill the process
lsof -ti:8000 | xargs kill -9  # Linux
taskkill /F /PID <PID>         # Windows
```

### Issue: Package installation fails

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Then retry
pip install -r requirements.txt
```

For more issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## Need Help?

- 📖 Full Setup Guide: [SETUP.md](SETUP.md)
- 🔧 Troubleshooting: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- 🐛 Report Issues: [GitHub Issues](https://github.com/Revoluz/MotoFix-Web-Based-OOP-Service-Manager-/issues)

---

## Pro Tips

1. **Always activate virtual environment** before running Django commands
2. **Use SQLite for development** (default), PostgreSQL for production
3. **Keep DEBUG=True** only in development
4. **Backup your database** before major migrations
5. **Read the full SETUP.md** for production deployment

Happy coding! 🚀
