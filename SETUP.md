# MotoFix - Web Based OOP Service Manager

Aplikasi web berorientasi objek yang berfungsi sebagai sistem ticketing dan invoicing untuk layanan perawatan kendaraan roda dua.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
  - [Windows Setup](#windows-setup)
  - [Linux Ubuntu Setup](#linux-ubuntu-setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Features
- Ticketing system for motorcycle service requests
- Invoice generation and management
- Object-oriented architecture
- User management and authentication
- Service history tracking

## Requirements

### Common Requirements (All Platforms)
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Optional
- PostgreSQL (for production, SQLite is used for development by default)
- Virtual environment tool (venv, virtualenv, or conda)

---

## Setup Instructions

### Windows Setup

#### Prerequisites
1. **Install Python:**
   - Download Python from [python.org](https://www.python.org/downloads/)
   - During installation, **check "Add Python to PATH"**
   - Verify installation:
     ```cmd
     python --version
     pip --version
     ```

2. **Install Git:**
   - Download from [git-scm.com](https://git-scm.com/download/win)
   - Install with default settings

#### Installation Steps

1. **Clone the repository:**
   ```cmd
   git clone https://github.com/Revoluz/MotoFix-Web-Based-OOP-Service-Manager-.git
   cd MotoFix-Web-Based-OOP-Service-Manager-
   ```

2. **Create virtual environment:**
   ```cmd
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```
   
   You should see `(venv)` prefix in your command prompt.

4. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Create environment file:**
   ```cmd
   copy .env.example .env
   ```
   
   Or create `.env` file manually with:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

6. **Run migrations:**
   ```cmd
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser:**
   ```cmd
   python manage.py createsuperuser
   ```

8. **Run the development server:**
   ```cmd
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` in your browser.

#### Alternative: Using the Setup Script

Run the automated setup script:
```cmd
setup_windows.bat
```

---

### Linux Ubuntu Setup

#### Prerequisites
1. **Update system packages:**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Install Python and pip:**
   ```bash
   sudo apt install python3 python3-pip python3-venv -y
   ```

3. **Verify installation:**
   ```bash
   python3 --version
   pip3 --version
   ```

4. **Install Git:**
   ```bash
   sudo apt install git -y
   ```

#### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Revoluz/MotoFix-Web-Based-OOP-Service-Manager-.git
   cd MotoFix-Web-Based-OOP-Service-Manager-
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```
   
   You should see `(venv)` prefix in your terminal.

4. **Upgrade pip (recommended):**
   ```bash
   pip install --upgrade pip
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Create environment file:**
   ```bash
   cp .env.example .env
   ```
   
   Or create `.env` file manually:
   ```bash
   cat > .env << EOF
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   EOF
   ```

7. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

9. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` in your browser.

#### Alternative: Using the Setup Script

Make the script executable and run it:
```bash
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

---

## Running the Application

### Start Development Server
**Windows:**
```cmd
venv\Scripts\activate
python manage.py runserver
```

**Linux:**
```bash
source venv/bin/activate
python manage.py runserver
```

### Access the Application
- Main application: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

### Deactivate Virtual Environment
When you're done:
```bash
deactivate
```

---

## Project Structure

```
MotoFix-Web-Based-OOP-Service-Manager-/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── setup_windows.bat        # Windows setup script
├── setup_ubuntu.sh          # Linux setup script
├── motofix/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI config
│   └── asgi.py              # ASGI config
├── apps/                    # Application modules
│   ├── tickets/             # Ticketing system
│   ├── invoices/            # Invoice management
│   ├── users/               # User management
│   └── vehicles/            # Vehicle information
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
└── templates/               # HTML templates
```

---

## Common Issues and Solutions

### Windows Issues

1. **"python is not recognized"**
   - Ensure Python is added to PATH during installation
   - Restart Command Prompt after installation

2. **Virtual environment activation fails**
   - Run as Administrator
   - Or use: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

3. **pip install fails**
   - Upgrade pip: `python -m pip install --upgrade pip`
   - Use administrator privileges

### Linux Issues

1. **Permission denied**
   - Use `sudo` for system-wide installations
   - Or ensure proper permissions: `sudo chown -R $USER:$USER .`

2. **python3-venv not found**
   - Install: `sudo apt install python3-venv`

3. **Database errors**
   - Ensure SQLite is installed (usually comes with Python)
   - For PostgreSQL, install: `sudo apt install postgresql postgresql-contrib`

---

## Development Tools

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
```

### Database Shell
```bash
python manage.py dbshell
```

### Django Shell
```bash
python manage.py shell
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Contact

Project Link: [https://github.com/Revoluz/MotoFix-Web-Based-OOP-Service-Manager-](https://github.com/Revoluz/MotoFix-Web-Based-OOP-Service-Manager-)
