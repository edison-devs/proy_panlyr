from django.core.management.base import BaseCommand
from core.models import (
    Category,
    PaymentMethod,
    CartStatus,
    OrderType,
    DeliveryStatus,
    OutputReason
)


class Command(BaseCommand):
    help = 'Seed initial data for categories, payment methods, statuses, etc only if they do not exist'

    def handle(self, *args, **kwargs):
        self.seed_data(Category, [
            {"name": "Galleta", "description": "Dulces horneados, diferentes sabores"},
            {"name": "Pan", "description": ""},
            {"name": "Repostería", "description": "Tortas, pasteles y postres"},
        ], "Categorías")

        self.seed_data(PaymentMethod, [
            {"name": "Efectivo", "description": "Pago en efectivo al recibir el pedido"},
            {"name": "Transferencia", "description": "Transferencia bancaria o digital"},
        ], "Métodos de pago")

        self.seed_data(CartStatus, [
            {"name": "Activo", "description": "Carrito en uso, pendiente de confirmación"},
            {"name": "Pendiente", "description": "Carrito guardado sin confirmar"},
            {"name": "Cancelado", "description": "Carrito cancelado por el usuario"},
        ], "Estados de carrito")

        self.seed_data(OrderType, [
            {"name": "Entregado", "description": "Pedido para entregar en el momento"},
            {"name": "Pendiente", "description": "Pedido con fecha y hora programada"},
        ], "Tipos de pedido")

        self.seed_data(DeliveryStatus, [
            {"name": "Entrega inmediata", "description": "Aún no ha sido entregado"},
            {"name": "Domicilio", "description": "Repartidor salió con el pedido"},
            {"name": "Entregado", "description": "El cliente recibió el pedido"},
        ], "Estados de entrega")

        self.seed_data(OutputReason, [
            {"name": "Vendido", "description": "Producto vendido a un cliente"},
            {"name": "Consumo de la casa", "description": "Consumido dentro de la panadería"},
            {"name": "Mal estado", "description": "Producto dañado o vencido"},
        ], "Motivos de salida")

    def seed_data(self, model, data, label):
        """
        Inserta datos iniciales en el modelo indicado si no existen.
        """
        for entry in data:
            existing = model.objects.filter(name=entry["name"]).first()

            if existing:
                if existing.description == entry["description"]:
                    self.stdout.write(
                        self.style.WARNING(f'{label}: "{entry["name"]}" ya existe con datos coincidentes')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'{label}: "{entry["name"]}" existe pero con campos distintos')
                    )
            else:
                model.objects.create(**entry)
                self.stdout.write(
                    self.style.SUCCESS(f'{label}: creado "{entry["name"]}"')
                )

