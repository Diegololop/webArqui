from django.core.management.base import BaseCommand, CommandError
from ...models import Product

class Command(BaseCommand):
    help = 'Crear productos en el sistema'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Nombre del producto')
        parser.add_argument('description', type=str, help='Descripción del producto')
        parser.add_argument('price', type=float, help='Precio del producto')
        parser.add_argument('stock', type=int, help='Cantidad en inventario')
        parser.add_argument('category', type=str, choices=['product', 'service'], help='Categoría del producto (product o service)')
        parser.add_argument('image_path', type=str, nargs='?', default=None, help='Ruta de la imagen (opcional)')

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        description = kwargs['description']
        price = kwargs['price']
        stock = kwargs['stock']
        category = kwargs['category']
        image_path = kwargs.get('image_path')

        # Validar si el producto ya existe
        if Product.objects.filter(name=name).exists():
            raise CommandError(f"El producto '{name}' ya existe.")

        # Crear el producto
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category
        )

        # Agregar la imagen si se proporciona
        if image_path:
            try:
                with open(image_path, 'rb') as img_file:
                    product.image.save(image_path.split('/')[-1], img_file)
            except FileNotFoundError:
                self.stderr.write(f"Imagen no encontrada: {image_path}")
                product.image = None

        product.save()
        self.stdout.write(self.style.SUCCESS(f"Producto '{name}' creado con éxito."))
