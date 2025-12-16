# Contributing to MotoFix

Thank you for your interest in contributing to MotoFix! This document provides guidelines and instructions for contributing to this project.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

---

## Getting Started

### Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher
- Git
- A GitHub account
- Basic knowledge of Django and Python

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/MotoFix-Web-Based-OOP-Service-Manager-.git
   cd MotoFix-Web-Based-OOP-Service-Manager-
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/Revoluz/MotoFix-Web-Based-OOP-Service-Manager-.git
   ```

---

## Development Setup

### 1. Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

---

## Making Changes

### Create a Branch

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - for new features
- `fix/` - for bug fixes
- `docs/` - for documentation changes
- `refactor/` - for code refactoring
- `test/` - for adding tests

### Keep Your Branch Updated

Regularly sync with the upstream repository:

```bash
git fetch upstream
git rebase upstream/main
```

---

## Coding Standards

### Python Style Guide

We follow PEP 8 style guide:

- Use 4 spaces for indentation (not tabs)
- Maximum line length: 79 characters
- Use descriptive variable names
- Add docstrings to classes and functions

### Django Best Practices

- Follow Django's coding style
- Use Django's built-in features and ORM
- Keep views lean, use models for business logic
- Use Django forms for data validation
- Write reusable apps when possible

### Example:

```python
class MotorcycleService(models.Model):
    """Model representing a motorcycle service request."""
    
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Motorcycle Service'
        verbose_name_plural = 'Motorcycle Services'
    
    def __str__(self):
        return f"{self.service_type} - {self.vehicle}"
```

### Code Formatting

Use these tools to maintain code quality:

```bash
# Format code with Black
pip install black
black .

# Check PEP 8 compliance
pip install flake8
flake8 .

# Sort imports
pip install isort
isort .
```

---

## Testing

### Write Tests

All new features should include tests:

```python
from django.test import TestCase
from .models import MotorcycleService

class MotorcycleServiceTestCase(TestCase):
    def setUp(self):
        # Setup test data
        pass
    
    def test_service_creation(self):
        """Test creating a new service"""
        # Your test code here
        pass
```

### Run Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test apps.tickets

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Submitting Changes

### Commit Guidelines

Write clear, descriptive commit messages:

```bash
# Good commit messages:
git commit -m "Add invoice generation feature"
git commit -m "Fix: Resolve ticket status update bug"
git commit -m "Docs: Update setup instructions for Windows"

# Bad commit messages:
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

Commit message format:
```
Type: Short description (50 chars or less)

Detailed explanation if necessary. Wrap at 72 characters.
Include the motivation for the change and contrast with
previous behavior.

- Bullet points are okay
- Use imperative mood: "Add feature" not "Added feature"
```

Types:
- `Add:` - New feature
- `Fix:` - Bug fix
- `Docs:` - Documentation changes
- `Style:` - Code style changes (formatting, etc.)
- `Refactor:` - Code refactoring
- `Test:` - Adding tests
- `Chore:` - Maintenance tasks

### Push Changes

```bash
git push origin feature/your-feature-name
```

### Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template:
   - **Title:** Clear, descriptive title
   - **Description:** What changes were made and why
   - **Related Issues:** Link any related issues
   - **Testing:** How you tested the changes
   - **Screenshots:** If UI changes were made

### Pull Request Checklist

Before submitting, ensure:
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated if needed
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main
- [ ] No merge conflicts

---

## Code Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Celebrate! 🎉

### Responding to Feedback

- Be open to suggestions
- Ask questions if something is unclear
- Make requested changes in new commits
- Push updates to the same branch

---

## Project Structure

Understanding the project structure:

```
MotoFix/
├── manage.py                 # Django management
├── requirements.txt          # Dependencies
├── motofix/                  # Main project
│   ├── settings.py          # Settings
│   ├── urls.py              # Root URLs
│   └── wsgi.py              # WSGI config
├── apps/                    # Django apps
│   ├── tickets/             # Ticketing system
│   │   ├── models.py       # Database models
│   │   ├── views.py        # View logic
│   │   ├── urls.py         # URL routing
│   │   ├── forms.py        # Forms
│   │   └── tests.py        # Tests
│   ├── invoices/            # Invoice management
│   ├── users/               # User management
│   └── vehicles/            # Vehicle info
├── static/                  # Static files
├── templates/               # HTML templates
└── media/                   # Uploaded files
```

---

## Common Tasks

### Adding a New Feature

1. Create a new branch
2. Implement the feature
3. Write tests
4. Update documentation
5. Submit PR

### Fixing a Bug

1. Create a new branch
2. Write a test that reproduces the bug
3. Fix the bug
4. Verify the test passes
5. Submit PR

### Updating Documentation

1. Create a new branch
2. Make documentation changes
3. Preview changes locally
4. Submit PR

---

## Getting Help

If you need help:

- Check existing [Issues](https://github.com/Revoluz/MotoFix-Web-Based-OOP-Service-Manager-/issues)
- Ask questions in discussions
- Read the documentation:
  - [SETUP.md](SETUP.md)
  - [QUICKSTART.md](QUICKSTART.md)
  - [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## Recognition

Contributors will be recognized in:
- README.md (Contributors section)
- Release notes for major contributions

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to MotoFix! 🚀
