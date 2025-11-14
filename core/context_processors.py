# context_processors.py
from .models import Cart, CartStatus


def cart_context(request):
    """Context processor para agregar información del carrito a todos los templates"""
    cart_items_count = 0
    if request.user.is_authenticated:
        try:
            # Se usa iexact para evitar bug al filtrar el nombre de la categoria del pedido
            status_pendiente = CartStatus.objects.filter(name__iexact="pendiente").first()
            if status_pendiente:
                cart = Cart.objects.filter(
                    user=request.user,
                    status=status_pendiente,
                    deleted_at__isnull=True
                ).first()
                if cart:
                    cart_items_count = cart.get_total_quantity()
        except Exception:
            # Si hay algún error, simplemente retornar 0
            cart_items_count = 0
    
    return {
        'cart_items_count': cart_items_count,
    }

