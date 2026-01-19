from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create demo users for testing and development'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo users...')
        
        # List of demo users to create
        demo_users = [
            {
                'username': 'admin',
                'email': 'admin@motofix.com',
                'password': 'admin123',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'MotoFix',
                'phone': '081234567890',
            },
            {
                'username': 'kasir',
                'email': 'kasir@motofix.com',
                'password': 'kasir123',
                'role': 'cashier',
                'first_name': 'Kasir',
                'last_name': 'MotoFix',
                'phone': '081234567891',
            },
            {
                'username': 'mekanik',
                'email': 'mekanik@motofix.com',
                'password': 'mekanik123',
                'role': 'mechanic',
                'first_name': 'Mekanik',
                'last_name': 'MotoFix',
                'phone': '081234567892',
            },
            {
                'username': 'customer',
                'email': 'customer@motofix.com',
                'password': 'customer123',
                'role': 'customer',
                'first_name': 'Customer',
                'last_name': 'Demo',
                'phone': '081234567893',
                'address': 'Jl. Contoh No. 123, Jakarta',
            },
        ]
        
        created_count = 0
        skipped_count = 0
        
        for user_data in demo_users:
            username = user_data['username']
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists, skipping...')
                )
                skipped_count += 1
                continue
            
            # Create user
            password = user_data.pop('password')
            user = User.objects.create(**user_data)
            user.set_password(password)
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Created user: {username} (role: {user_data["role"]})')
            )
            created_count += 1
        
        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done! Created {created_count} users, skipped {skipped_count} existing users.'))
        
        if created_count > 0:
            self.stdout.write('')
            self.stdout.write('Demo credentials:')
            self.stdout.write('  Admin:    admin    / admin123')
            self.stdout.write('  Kasir:    kasir    / kasir123')
            self.stdout.write('  Mekanik:  mekanik  / mekanik123')
            self.stdout.write('  Customer: customer / customer123')
