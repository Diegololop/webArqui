from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from workshop.models import (
    UserProfile, Client, Product, WorkOrder, WorkOrderNote,
    Reservation, Provider, BusinessHours
)
from datetime import timedelta, datetime
import random

class Command(BaseCommand):
    help = 'Creates sample data for all models'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create sample users and profiles
        self.create_users()
        
        # Create sample clients
        self.create_clients()
        
        # Create sample products and services
        self.create_products_and_services()
        
        # Create sample providers
        self.create_providers()
        
        # Create sample work orders
        self.create_work_orders()
        
        # Create sample reservations
        self.create_reservations()

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))

    def create_users(self):
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            UserProfile.objects.create(user=admin, role='admin', phone='+56912345678')

        # Create mechanics
        mechanic_names = [
            ('Juan', 'Pérez'), ('Pedro', 'González'), ('María', 'López')
        ]
        for first_name, last_name in mechanic_names:
            username = f'{first_name.lower()}.{last_name.lower()}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='mechanic123',
                    first_name=first_name,
                    last_name=last_name
                )
                UserProfile.objects.create(user=user, role='mechanic', phone='+56912345678')

        # Create receptionist
        if not User.objects.filter(username='receptionist').exists():
            user = User.objects.create_user(
                username='receptionist',
                email='receptionist@example.com',
                password='reception123',
                first_name='Ana',
                last_name='Silva'
            )
            UserProfile.objects.create(user=user, role='receptionist', phone='+56912345678')

    def create_clients(self):
        client_data = [
            {
                'username': 'cliente1',
                'email': 'cliente1@example.com',
                'first_name': 'Carlos',
                'last_name': 'Rodríguez',
                'rut': '12.345.678-9',
                'phone': '+56987654321',
                'address': 'Av. Principal 123'
            },
            {
                'username': 'cliente2',
                'email': 'cliente2@example.com',
                'first_name': 'Laura',
                'last_name': 'Martínez',
                'rut': '11.222.333-4',
                'phone': '+56998765432',
                'address': 'Calle Secundaria 456'
            },
            {
                'username': 'cliente3',
                'email': 'cliente3@example.com',
                'first_name': 'Diego',
                'last_name': 'Sánchez',
                'rut': '10.111.222-3',
                'phone': '+56976543210',
                'address': 'Pasaje Los Pinos 789'
            }
        ]

        for data in client_data:
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password='client123',
                    first_name=data['first_name'],
                    last_name=data['last_name']
                )
                Client.objects.create(
                    user=user,
                    rut=data['rut'],
                    phone=data['phone'],
                    address=data['address']
                )

    def create_products_and_services(self):
        services = [
            {
                'name': 'Cambio de Aceite',
                'description': 'Servicio completo de cambio de aceite y filtro',
                'price': 45000,
                'category': 'service',
                'duration': 30,
                'stock': 999
            },
            {
                'name': 'Alineación y Balanceo',
                'description': 'Servicio de alineación computarizada y balanceo',
                'price': 35000,
                'category': 'service',
                'duration': 45,
                'stock': 999
            },
            {
                'name': 'Revisión de Frenos',
                'description': 'Inspección completa del sistema de frenos',
                'price': 25000,
                'category': 'service',
                'duration': 60,
                'stock': 999
            }
        ]

        products = [
            {
                'name': 'Aceite de Motor',
                'description': 'Aceite sintético 5W-30',
                'price': 25000,
                'category': 'product',
                'stock': 50
            },
            {
                'name': 'Filtro de Aceite',
                'description': 'Filtro de aceite universal',
                'price': 8000,
                'category': 'product',
                'stock': 100
            },
            {
                'name': 'Pastillas de Freno',
                'description': 'Juego de pastillas de freno delanteras',
                'price': 35000,
                'category': 'product',
                'stock': 30
            }
        ]

        for service in services:
            Product.objects.get_or_create(
                name=service['name'],
                defaults=service
            )

        for product in products:
            Product.objects.get_or_create(
                name=product['name'],
                defaults=product
            )

    def create_providers(self):
        providers = [
            {
                'name': 'Repuestos Automotrices S.A.',
                'rut': '76.543.210-K',
                'email': 'contacto@repuestos.cl',
                'phone': '+56922334455',
                'address': 'Av. Industrial 1234',
                'description': 'Proveedor principal de repuestos originales'
            },
            {
                'name': 'Lubricantes del Sur',
                'rut': '77.666.555-4',
                'email': 'ventas@lubricantes.cl',
                'phone': '+56933445566',
                'address': 'Calle Comercio 567',
                'description': 'Distribuidor autorizado de aceites y lubricantes'
            },
            {
                'name': 'Neumáticos Express',
                'rut': '78.999.888-7',
                'email': 'ventas@neumaticos.cl',
                'phone': '+56944556677',
                'address': 'Av. Principal 890',
                'description': 'Proveedor especializado en neumáticos'
            }
        ]

        for provider_data in providers:
            Provider.objects.get_or_create(
                rut=provider_data['rut'],
                defaults=provider_data
            )

    def create_work_orders(self):
        clients = Client.objects.all()
        mechanics = UserProfile.objects.filter(role='mechanic')
        statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        
        for client in clients:
            for _ in range(random.randint(1, 3)):
                work_order = WorkOrder.objects.create(
                    client=client,
                    mechanic=random.choice(mechanics),
                    vehicle_model=random.choice(['Toyota Corolla', 'Nissan Versa', 'Hyundai Accent']),
                    vehicle_year=random.randint(2015, 2023),
                    description='Mantenimiento general del vehículo',
                    status=random.choice(statuses),
                    estimated_completion=timezone.now() + timedelta(days=random.randint(1, 7)),
                    total_cost=random.randint(50000, 500000)
                )

                # Add some notes
                WorkOrderNote.objects.create(
                    work_order=work_order,
                    user=work_order.mechanic.user,
                    note='Inspección inicial realizada'
                )

    def create_reservations(self):
        clients = Client.objects.all()
        services = Product.objects.filter(category='service')
        
        for client in clients:
            for _ in range(random.randint(1, 2)):
                selected_services = random.sample(list(services), random.randint(1, 3))
                total_duration = sum(service.duration or 0 for service in selected_services)
                total_price = sum(service.price for service in selected_services)
                
                reservation = Reservation.objects.create(
                    client=client,
                    service_date=timezone.now() + timedelta(days=random.randint(1, 14)),
                    description='Reserva para mantenimiento',
                    status=random.choice(['pending', 'confirmed', 'cancelled']),
                    total_duration=total_duration,
                    total_price=total_price
                )
                reservation.services.set(selected_services)