# MotoFix-Web-Based-OOP-Service-Manager-

Aplikasi web berorientasi objek yang berfungsi sebagai sistem ticketing dan invoicing untuk layanan perawatan kendaraan roda dua.

## Quick Start

This project supports both Windows and Linux (Ubuntu) platforms.

### Automated Setup

**Windows:**
```cmd
setup_windows.bat
```

**Linux/Ubuntu:**
```bash
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

### Manual Setup

For detailed setup instructions, please refer to [SETUP.md](SETUP.md).

## Features

- 🎫 Ticketing system for motorcycle service requests
- 💰 Invoice generation and management
- 🏗️ Object-oriented architecture
- 👥 User management and authentication
- 📊 Service history tracking

## Documentation

- [Complete Setup Guide](SETUP.md) - Detailed setup instructions for Windows and Linux
- [Requirements](requirements.txt) - Python package dependencies

## Tech Stack

- Python 3.8+
- Django 4.2+
- SQLite (development) / PostgreSQL (production)
- Bootstrap 5
- Django REST Framework

## Quick Commands

After setup, use these commands:

```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# Linux: source venv/bin/activate

# Run development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
