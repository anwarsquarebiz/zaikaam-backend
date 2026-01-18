"""
Django management command to seed User table with dummy users and their profiles.

Usage:
    python manage.py seed_users
    python manage.py seed_users --reset  # Reset existing users (will delete and recreate them)
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed User table with dummy users and their profiles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset existing dummy users before seeding (WARNING: This will delete users and their data!)',
        )

    def handle(self, *args, **options):
        reset = options['reset']

        # Define dummy users with Indian names and details
        users_data = [
            # Admin users
            {
                'username': 'admin',
                'email': 'admin@cateringplatform.com',
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'role': 'admin',
                'phone': '+91-9876543210',
                'password': 'admin123',
                'is_staff': True,
                'is_superuser': True,
                'profile': {
                    'city': 'Mumbai',
                    'address': 'Admin Office, Bandra West, Mumbai - 400050',
                }
            },
            {
                'username': 'admin2',
                'email': 'admin2@cateringplatform.com',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'role': 'admin',
                'phone': '+91-9876543211',
                'password': 'admin123',
                'is_staff': True,
                'is_superuser': False,
                'profile': {
                    'city': 'Delhi',
                    'address': 'Corporate Office, Connaught Place, New Delhi - 110001',
                }
            },

            # Customer users
            {
                'username': 'customer1',
                'email': 'rahul.verma@email.com',
                'first_name': 'Rahul',
                'last_name': 'Verma',
                'role': 'customer',
                'phone': '+91-9876543201',
                'password': 'customer123',
                'profile': {
                    'city': 'Mumbai',
                    'address': 'Flat 501, Sea View Apartments, Juhu, Mumbai - 400049',
                }
            },
            {
                'username': 'customer2',
                'email': 'priya.patel@email.com',
                'first_name': 'Priya',
                'last_name': 'Patel',
                'role': 'customer',
                'phone': '+91-9876543202',
                'password': 'customer123',
                'profile': {
                    'city': 'Delhi',
                    'address': 'House No. 25, Defence Colony, New Delhi - 110024',
                }
            },
            {
                'username': 'customer3',
                'email': 'amit.singh@email.com',
                'first_name': 'Amit',
                'last_name': 'Singh',
                'role': 'customer',
                'phone': '+91-9876543203',
                'password': 'customer123',
                'profile': {
                    'city': 'Bangalore',
                    'address': '123, MG Road, Bangalore - 560001',
                }
            },
            {
                'username': 'customer4',
                'email': 'neha.gupta@email.com',
                'first_name': 'Neha',
                'last_name': 'Gupta',
                'role': 'customer',
                'phone': '+91-9876543204',
                'password': 'customer123',
                'profile': {
                    'city': 'Pune',
                    'address': 'Flat 202, Koregaon Park, Pune - 411001',
                }
            },
            {
                'username': 'customer5',
                'email': 'vikram.reddy@email.com',
                'first_name': 'Vikram',
                'last_name': 'Reddy',
                'role': 'customer',
                'phone': '+91-9876543205',
                'password': 'customer123',
                'profile': {
                    'city': 'Hyderabad',
                    'address': 'House No. 45, Banjara Hills, Hyderabad - 500034',
                }
            },
            {
                'username': 'customer6',
                'email': 'kavita.malhotra@email.com',
                'first_name': 'Kavita',
                'last_name': 'Malhotra',
                'role': 'customer',
                'phone': '+91-9876543206',
                'password': 'customer123',
                'profile': {
                    'city': 'Gurgaon',
                    'address': 'Sector 44, Gurgaon - 122002',
                }
            },
            {
                'username': 'customer7',
                'email': 'rohan.desai@email.com',
                'first_name': 'Rohan',
                'last_name': 'Desai',
                'role': 'customer',
                'phone': '+91-9876543207',
                'password': 'customer123',
                'profile': {
                    'city': 'Ahmedabad',
                    'address': '101, C.G. Road, Ahmedabad - 380006',
                }
            },
            {
                'username': 'customer8',
                'email': 'divya.nair@email.com',
                'first_name': 'Divya',
                'last_name': 'Nair',
                'role': 'customer',
                'phone': '+91-9876543208',
                'password': 'customer123',
                'profile': {
                    'city': 'Chennai',
                    'address': 'Flat 305, T. Nagar, Chennai - 600017',
                }
            },
            {
                'username': 'customer9',
                'email': 'arjun.mehta@email.com',
                'first_name': 'Arjun',
                'last_name': 'Mehta',
                'role': 'customer',
                'phone': '+91-9876543209',
                'password': 'customer123',
                'profile': {
                    'city': 'Kolkata',
                    'address': 'Park Street, Kolkata - 700016',
                }
            },
            {
                'username': 'customer10',
                'email': 'sneha.kapoor@email.com',
                'first_name': 'Sneha',
                'last_name': 'Kapoor',
                'role': 'customer',
                'phone': '+91-9876543212',
                'password': 'customer123',
                'profile': {
                    'city': 'Chandigarh',
                    'address': 'Sector 17, Chandigarh - 160017',
                }
            },

            # Vendor users
            {
                'username': 'vendor1',
                'email': 'royal.kitchen@catering.com',
                'first_name': 'Raj',
                'last_name': 'Khanna',
                'role': 'vendor',
                'phone': '+91-9876543301',
                'password': 'vendor123',
                'profile': {
                    'city': 'Mumbai',
                    'address': 'Royal Kitchen, Andheri West, Mumbai - 400053',
                }
            },
            {
                'username': 'vendor2',
                'email': 'spice.route@catering.com',
                'first_name': 'Anjali',
                'last_name': 'Srinivasan',
                'role': 'vendor',
                'phone': '+91-9876543302',
                'password': 'vendor123',
                'profile': {
                    'city': 'Bangalore',
                    'address': 'Spice Route, Indira Nagar, Bangalore - 560038',
                }
            },
            {
                'username': 'vendor3',
                'email': 'tandoor.kitchen@catering.com',
                'first_name': 'Mohammed',
                'last_name': 'Ali',
                'role': 'vendor',
                'phone': '+91-9876543303',
                'password': 'vendor123',
                'profile': {
                    'city': 'Delhi',
                    'address': 'Tandoor Kitchen, Karol Bagh, New Delhi - 110005',
                }
            },
            {
                'username': 'vendor4',
                'email': 'south.spice@catering.com',
                'first_name': 'Karthik',
                'last_name': 'Iyer',
                'role': 'vendor',
                'phone': '+91-9876543304',
                'password': 'vendor123',
                'profile': {
                    'city': 'Chennai',
                    'address': 'South Spice, Anna Nagar, Chennai - 600040',
                }
            },
            {
                'username': 'vendor5',
                'email': 'gujarati.thali@catering.com',
                'first_name': 'Harsh',
                'last_name': 'Patel',
                'role': 'vendor',
                'phone': '+91-9876543305',
                'password': 'vendor123',
                'profile': {
                    'city': 'Ahmedabad',
                    'address': 'Gujarati Thali House, Navrangpura, Ahmedabad - 380009',
                }
            },

            # Support users
            {
                'username': 'support1',
                'email': 'support@cateringplatform.com',
                'first_name': 'Anita',
                'last_name': 'Joshi',
                'role': 'support',
                'phone': '+91-9876543401',
                'password': 'support123',
                'profile': {
                    'city': 'Mumbai',
                    'address': 'Support Center, Andheri East, Mumbai - 400069',
                }
            },
            {
                'username': 'support2',
                'email': 'support2@cateringplatform.com',
                'first_name': 'Suresh',
                'last_name': 'Kumar',
                'role': 'support',
                'phone': '+91-9876543402',
                'password': 'support123',
                'profile': {
                    'city': 'Delhi',
                    'address': 'Support Office, Nehru Place, New Delhi - 110019',
                }
            },
        ]

        if reset:
            self.stdout.write(self.style.WARNING('⚠️  WARNING: This will delete all users except superusers!'))
            # Delete only non-superuser users to be safe
            deleted_users = User.objects.filter(is_superuser=False).delete()
            deleted_count = deleted_users[0] if deleted_users else 0
            self.stdout.write(
                self.style.SUCCESS(f'Deleted {deleted_count} existing users.')
            )

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for user_data in users_data:
            username = user_data['username']
            profile_data = user_data.pop('profile', None)
            password = user_data.pop('password')

            try:
                # Create or update user
                user, created = User.objects.update_or_create(
                    username=username,
                    defaults={
                        'email': user_data['email'],
                        'first_name': user_data['first_name'],
                        'last_name': user_data['last_name'],
                        'role': user_data['role'],
                        'phone': user_data.get('phone', ''),
                        'is_staff': user_data.get('is_staff', False),
                        'is_superuser': user_data.get('is_superuser', False),
                        'is_active': True,
                    }
                )

                # Set password (this will hash it properly)
                user.set_password(password)
                user.save()

                # Create or update profile if provided
                if profile_data:
                    profile, profile_created = Profile.objects.update_or_create(
                        user=user,
                        defaults={
                            'city': profile_data['city'],
                            'address': profile_data.get('address', ''),
                        }
                    )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created: {username} ({user_data["role"]})')
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'↻ Updated: {username} ({user_data["role"]})')
                    )
            except Exception as e:
                skipped_count += 1
                self.stdout.write(
                    self.style.ERROR(f'✗ Error processing {username}: {str(e)}')
                )

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))
        self.stdout.write(self.style.SUCCESS('Seeding Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  Created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Updated: {updated_count}'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'  Skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))

        # Role-wise summary
        admin_count = User.objects.filter(role='admin').count()
        customer_count = User.objects.filter(role='customer').count()
        vendor_count = User.objects.filter(role='vendor').count()
        support_count = User.objects.filter(role='support').count()

        self.stdout.write(self.style.SUCCESS('\nRole-wise User Count:'))
        self.stdout.write(self.style.SUCCESS(f'  Admin: {admin_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Customer: {customer_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Vendor: {vendor_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Support: {support_count}'))

        total_users = User.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal users in database: {total_users}')
        )

        # Default passwords reminder
        self.stdout.write(self.style.WARNING('\n📝 Default Passwords:'))
        self.stdout.write(self.style.WARNING('  Admin: admin123'))
        self.stdout.write(self.style.WARNING('  Customer: customer123'))
        self.stdout.write(self.style.WARNING('  Vendor: vendor123'))
        self.stdout.write(self.style.WARNING('  Support: support123'))
        self.stdout.write(
            self.style.WARNING('\n⚠️  Please change these passwords in production!')
        )


