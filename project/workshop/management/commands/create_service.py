from django.core.management.base import BaseCommand
from ...models import Product  # Reemplaza "app" con el nombre de tu aplicación

class Command(BaseCommand):
    help = "Crea un nuevo servicio en el sistema"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Nombre del servicio')
        parser.add_argument('description', type=str, help='Descripción del servicio')
        parser.add_argument('price', type=float, help='Precio del servicio')
        parser.add_argument('duration', type=int, help='Duración estimada en minutos')

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        description = kwargs['description']
        price = kwargs['price']
        duration = kwargs['duration']

        service = Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=0,  # Los servicios no tienen stock
            category='service',
            duration=duration
        )

        self.stdout.write(self.style.SUCCESS(f'Servicio creado: {service.name} (ID: {service.id})'))
