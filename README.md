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

- Ticketing system for motorcycle service requests
- Invoice generation and management
- Object-oriented architecture
- User management and authentication with role-based access
- Service history tracking
- Automated payment calculation with change
- Invoice printing system

## Demo Users

After setup, run the seed command to create demo users:

```bash
python manage.py seed_users
```

This will create the following demo accounts:

| Role     | Username | Password    | Description           |
|----------|----------|-------------|-----------------------|
| Admin    | admin    | admin123    | Full system access    |
| Kasir    | kasir    | kasir123    | Cashier access        |
| Mekanik  | mekanik  | mekanik123  | Mechanic access       |
| Customer | customer | customer123 | Customer portal       |

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

# Run migrations
python manage.py migrate

# Create demo users (recommended for testing)
python manage.py seed_users

# Run development server
python manage.py runserver

# Create superuser (optional, if you need custom admin)
python manage.py createsuperuser
```

## First Time Setup

1. Run automated setup script (setup_windows.bat or setup_ubuntu.sh)
2. Activate virtual environment
3. Run migrations: `python manage.py migrate`
4. Create demo users: `python manage.py seed_users`
5. Start server: `python manage.py runserver`
6. Access at http://127.0.0.1:8000
7. Login with demo credentials (see Demo Users section above)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
