# context_processors.py
from .models import Cart, CartStatus
import logging #Indentificar desde que archivo se origino el error

logger = logging.getLogger(__name__)

def cart_context(request):
    """Context processor para agregar información del carrito a todos los templates"""

    # valores por defecto (SIEMPRE existen)
    cart_items_count = 0
    cart_total = 0
    cart_items = []

    if request.user.is_authenticated:
        try:
            # Se usa iexact para evitar bug al filtrar el nombre de la categoria del pedido
            status_pendiente = CartStatus.objects.filter(
                name__iexact="pendiente"
            ).first()

            if status_pendiente:
                cart = Cart.objects.filter(
                    user=request.user,
                    status=status_pendiente,
                    deleted_at__isnull=True
                ).first()

                if cart:
                    cart_items = cart.cart_products.select_related("product")
                    cart_items_count = cart.get_total_quantity()
                    cart_total = cart.get_total()

        except Exception:
            logger.exception(
                "Error en cart_context para user %s",
                request.user
            )
            # dejamos los valores por defecto (0, [])

    return {
        'cart_items_count': cart_items_count,
        'cart_total': cart_total,
        'cart_items': cart_items,
    }