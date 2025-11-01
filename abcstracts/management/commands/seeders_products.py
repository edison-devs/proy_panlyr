# abcstracts/management/commands/seeder_products.py

from django.core.management.base import BaseCommand
from core.models import Category, Product
from django.db import transaction

class Command(BaseCommand):
    help = "Seeder para poblar la tabla de productos de ejemplo"

    @transaction.atomic  # Garantiza que si algo falla, no se guarda nada en BD
    def handle(self, *args, **options):
        try:
            # Lista de productos de ejemplo
            products_data = [
                {
                    "category": "Panadería",
                    "name": "Pan Andino",
                    "price": 1.50,
                    "description": "Pan tradicional de la región andina.",
                },
                {
                    "category": "Panadería",
                    "name": "Baguette",
                    "price": 2.00,
                    "description": "Clásico pan francés crujiente.",
                },
                {
                    "category": "Repostería",
                    "name": "Torta de Chocolate",
                    "price": 10.00,
                    "description": "Bizcocho húmedo de chocolate con cobertura cremosa.",
                },
                {
                    "category": "Repostería",
                    "name": "Galletas de Avena",
                    "price": 3.50,
                    "description": "Galletas caseras con avena y pasas.",
                },
                {
                    "category": "Repostería",
                    "name": "cupcake",
                    "price": 1.00,
                    "description": "Ponques de chocolate.",
                },
            ]

            created_count = 0

            for data in products_data:
                try:
                    # Buscar categoría por nombre
                    category = Category.objects.get(name=data["category"])

                    # Crear producto si no existe
                    product, created = Product.objects.get_or_create(
                        category=category,
                        name=data["name"],
                        defaults={
                            "price": data["price"],
                            "description": data["description"],
                            "image": None,  # Imagen nula (puedes subirla desde el CRUD)
                        },
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(self.style.SUCCESS(f"Producto creado: {product.name}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Ya existía: {product.name}"))

                except Category.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"No existe la categoría: {data['category']}")
                    )

            self.stdout.write(
                self.style.SUCCESS(f"Seeder finalizado. Productos nuevos: {created_count}")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al ejecutar seeder: {str(e)}"))
