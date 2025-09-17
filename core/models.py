from django.db import models
from django.core.validators import FileExtensionValidator # Para la importacion de imagenes
from abcstracts.models import TimestampedMixin, SoftDeleteMixin # Models de app abcstracts
from auth_users.models import User # Importando models de auth_users



# Seeder models
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, default="",verbose_name="Descripción")

    class Meta:
        db_table = "categories"
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class PaymentMethod(TimestampedMixin, SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, default="",verbose_name="Descripción")

    class Meta:
        db_table = "payment_methods"
        verbose_name = "Método de pago"
        verbose_name_plural = "Métodos de pago"

    def __str__(self):
        return self.name


class CartStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, default="",verbose_name="Descripción")

    class Meta:
        db_table = "cart_statuses"
        verbose_name = "Estado de carrito"
        verbose_name_plural = "Estados de carrito"

    def __str__(self):
        return self.name


class OrderType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, default="",verbose_name="Descripción")

    class Meta:
        db_table = "order_types"
        verbose_name = "Tipo de pedido"
        verbose_name_plural = "Tipos de pedido"

    def __str__(self):
        return self.name


class DeliveryStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, default="",verbose_name="Descripción")

    class Meta:
        db_table = "delivery_statuses"
        verbose_name = "Estado de entrega"
        verbose_name_plural = "Estados de entrega"

    def __str__(self):
        return self.name


class OutputReason(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, default="",verbose_name="Descripción")

    class Meta:
        db_table = "output_reasons"
        verbose_name = "Motivo de la salida"
        verbose_name_plural = "Motivos de la salida"

    def __str__(self):
        return self.name


# Dependent models
class Product(TimestampedMixin, SoftDeleteMixin, models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    description = models.TextField(blank=True, null= True, verbose_name="Descripción")
    stock = models.IntegerField(default=0, verbose_name="Inventario")
    image = models.ImageField(
        upload_to="core/products/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])],
        blank=True,
        null=True,
        verbose_name="Imagen"
    )

    class Meta:
        db_table = "products"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Cart(SoftDeleteMixin, models.Model):
    status = models.ForeignKey(CartStatus, on_delete=models.PROTECT, related_name="carts")
    quantity = models.IntegerField(default=0, verbose_name="Cantidad")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")

    class Meta:
        db_table = "carts"
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"{self.quantity} - ${self.price}"


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="cart_products")
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, verbose_name="Carrito")
    quantity = models.IntegerField(default=0, verbose_name="Cantidad")

    class Meta:
        db_table = "cart_products"
        verbose_name = "Producto en carrito"
        verbose_name_plural = "Productos en carritos"

    def __str__(self):
        return f"{self.product}: {self.quantity}"


class Payment(TimestampedMixin, SoftDeleteMixin, models.Model):
    method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name="Método de pago")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")

    class Meta:
        db_table = "payments"
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"{self.method} - ${self.amount}"


class Delivery(TimestampedMixin, SoftDeleteMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuario")
    secondary_address = models.CharField(max_length=255, blank=True, verbose_name="Dirección secundaria")

    class Meta:
        db_table = "deliveries"
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"

    def __str__(self):
        return f"{self.user}: {self.secondary_address}"


class Order(TimestampedMixin, SoftDeleteMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuario")
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, verbose_name="Carrito")
    order_type = models.ForeignKey(OrderType, on_delete=models.PROTECT, verbose_name="Tipo de pedido")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name="Método de pago")
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, verbose_name="Entrega")

    class Meta:
        db_table = "orders"
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"{self.user} - {self.delivery}"


class Input(TimestampedMixin, SoftDeleteMixin, models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    quantity = models.IntegerField(default=0, verbose_name="Cantidad")
    description = models.TextField(blank=True, null=True,verbose_name="Descripción")

    class Meta:
        db_table = "inputs"
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"

    def __str__(self):
        return f"{self.product}: {self.quantity}"


class Output(TimestampedMixin, SoftDeleteMixin, models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name="Pedido")
    reason = models.ForeignKey(OutputReason, on_delete=models.PROTECT, verbose_name="Motivo de salida")
    quantity = models.IntegerField(default=0, verbose_name="Cantidad")
    description = models.TextField(blank=True, null=True,verbose_name="Descripción")

    class Meta:
        db_table = "outputs"
        verbose_name = "Salida"
        verbose_name_plural = "Salidas"

    def __str__(self):
        return f"{self.product}: {self.reason}"


"""
-PROTECT: Evita que se borre un registro si tiene dependencias activas.

Esto combina bien con soft_delete, porque nunca se borrará en cascada sin querer.
"""