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


# Dependent models
class Product(TimestampedMixin, SoftDeleteMixin, models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    description = models.TextField(blank=True, null= True, verbose_name="Descripción")
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
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="carts", verbose_name="Usuario", null=True, blank=True)
    status = models.ForeignKey(CartStatus, on_delete=models.PROTECT, related_name="carts")
    quantity = models.IntegerField(default=0, verbose_name="Cantidad")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio")

    class Meta:
        db_table = "carts"
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        user_str = str(self.user) if self.user else "Sin usuario"
        return f"{user_str} - {self.quantity} - ${self.price}"
    
    def calculate_total(self):
        """Calcula el total del carrito basado en los productos"""
        total = sum(item.product.price * item.quantity for item in self.cart_products.all())
        self.price = total
        self.quantity = sum(item.quantity for item in self.cart_products.all())
        self.save()
        return total
    
    def get_total(self):
        """Retorna el total sin guardar"""
        return sum(item.product.price * item.quantity for item in self.cart_products.all())
    
    def get_total_quantity(self):
        """Retorna la cantidad total de items en el carrito"""
        return sum(item.quantity for item in self.cart_products.all())


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="cart_products")
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, related_name="cart_products", verbose_name="Carrito")
    quantity = models.IntegerField(default=0, verbose_name="Cantidad")

    class Meta:
        db_table = "cart_products"
        verbose_name = "Producto en carrito"
        verbose_name_plural = "Productos en carritos"
        unique_together = ['cart', 'product']  # Evita duplicados

    def __str__(self):
        return f"{self.product}: {self.quantity}"
    
    def get_subtotal(self):
        """Calcula el subtotal de este item (precio * cantidad)"""
        return self.product.price * self.quantity


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
    comprobante_pago = models.FileField(
        upload_to="core/comprobantes/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "pdf", "webp"])],
        blank=True,
        null=True,
        verbose_name="Comprobante de pago"
    )

    class Meta:
        db_table = "orders"
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']  # Ordenar por fecha de creación, más reciente primero

    def __str__(self):
        fecha = self.created_at.strftime('%d/%m/%Y') if self.created_at else 'Sin fecha'
        return f"Pedido #{self.id} - {self.user} - {fecha}"
    
    def get_total(self):
        """Retorna el total del pedido basado en el carrito"""
        return self.cart.get_total()
    
    def get_total_quantity(self):
        """Retorna la cantidad total de items en el pedido"""
        return self.cart.get_total_quantity()
    
    def get_cart_items(self):
        """Retorna los items del carrito asociado al pedido"""
        return self.cart.cart_products.all()
    
    def is_pendiente(self):
        """Verifica si el pedido está pendiente"""
        if self.order_type:
            return self.order_type.name.lower() == "pendiente"
        return False
    
    def is_aprobado(self):
        """Verifica si el pedido está aprobado"""
        if self.order_type:
            return self.order_type.name.lower() in ["aprobado", "confirmado", "en proceso", "procesando"]
        return False
    
    def necesita_comprobante(self):
        """Verifica si el método de pago requiere comprobante (transferencia)"""
        if self.payment_method:
            metodo_nombre = self.payment_method.name.lower()
            return metodo_nombre in ["transferencia", "transferencia bancaria", "pago movil", "pago móvil"]
        return False
    
    def tiene_comprobante(self):
        """Verifica si el pedido ya tiene comprobante de pago subido"""
        return bool(self.comprobante_pago)
    
    def esperando_comprobante(self):
        """Verifica si el pedido está esperando comprobante de pago"""
        if self.order_type:
            nombre_tipo = self.order_type.name.lower()
            return nombre_tipo in ["comprobante de pago requerido", "comprobante requerido", "comprobante requerido"]
        return False


"""
-PROTECT: Evita que se borre un registro si tiene dependencias activas.

Esto combina bien con soft_delete, porque nunca se borrará en cascada sin querer.
"""