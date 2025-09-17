from django.core.management.base import BaseCommand
from core.models import Product, Category


class Command(BaseCommand):
    help = 'Seed initial data for products only if they do not exist'

    def handle(self, *args, **kwargs):
        self.seed_products()

    def seed_products(self):
        products = [
            {"name": "Pan Francés", "description": "Pan tradicional crujiente", "price": 0.50, "category": "Pan", "stock": 100},
            {"name": "Galleta de Chocolate", "description": "Clásica galleta con chispas de chocolate", "price": 0.30, "category": "Galleta", "stock": 200},
            {"name": "Torta de Vainilla", "description": "Repostería esponjosa con glaseado", "price": 5.00, "category": "Repostería", "stock": 15},
            {"name": "Croissant", "description": "Delicioso croissant de mantequilla", "price": 1.20, "category": "Pan", "stock": 50},
            {"name": "Donas Glaseadas", "description": "Suaves donas con glaseado de azúcar", "price": 0.80, "category": "Repostería", "stock": 40},
        ]

        for entry in products:
            category = Category.objects.filter(name=entry["category"]).first()
            if not category:
                self.stdout.write(
                    self.style.ERROR(f'⚠️ No existe la categoría "{entry["category"]}", omitiendo "{entry["name"]}"')
                )
                continue

            existing = Product.objects.filter(name=entry["name"]).first()
            if existing:
                if (
                    existing.description == entry["description"]
                    and existing.price == entry["price"]
                    and existing.category == category
                ):
                    self.stdout.write(
                        self.style.WARNING(f'Producto "{entry["name"]}" ya existe con datos coincidentes')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'Producto "{entry["name"]}" existe pero con campos distintos')
                    )
            else:
                Product.objects.create(
                    name=entry["name"],
                    description=entry["description"],
                    price=entry["price"],
                    stock=entry["stock"],
                    category=category
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✔️ Producto creado "{entry["name"]}"')
                    )