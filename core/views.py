# View de app core logica principal
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin #Para autenticacion de usuario
from django.contrib.auth import authenticate,login, get_user_model,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages                      # <- necesario para mostrar mensajes
from .models import *
from .forms import ProductForm, PedidoForm, ComprobantePagoForm


# Create your views here.


#Redirige al home
def render_home(request):
    try:
        return render(request, 'core/home.html')
    except Exception as e:
        messages.error(request, f'Error al cargar la página principal: {e}')
        # Aún devolvemos la misma plantilla para no romper la navegación
        return render(request, 'core/home.html')



#Logica para redirigir al panel de administración
@login_required
def dashboard(request):
        return render(request, 'core/sidebar/index.html')

# --------------------------------------------------------------------------------------------
# INDEX PRODUCT
# --------------------------------------------------------------------------------------------

class ProductListView(View):
    template_name = "core/sidebar/products/index.html"

    def get(self, request):
        query = request.GET.get("q", "").strip() # búsqueda
        products = Product.objects.all()

        if query:
            # Buscar por nombre o categoría
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        # Paginación (6 productos por página)
        paginator = Paginator(products, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "query": query,
            "result_count": products.count()
        }
        return render(request, self.template_name, context)


# --------------------------------------------------------------------------------------------
# CREATE PRODUCT
# --------------------------------------------------------------------------------------------

class ProductCreateView(View):
    template_name = "core/sidebar/products/create.html"

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                return redirect("product-create")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al crear el producto: {e}")
        return render(request, self.template_name, {"form": form})


# --------------------------------------------------------------------------------------------
# UPDATE PRODUCT
# --------------------------------------------------------------------------------------------

class ProductUpdateView(View):
    template_name = "core/sidebar/products/update.html"

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Producto actualizado correctamente.")
                return redirect("product-index")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al actualizar: {e}")
        return render(request, self.template_name, {"form": form})


# --------------------------------------------------------------------------------------------
# DELETE PRODUCT
# --------------------------------------------------------------------------------------------

class ProductDeleteView(LoginRequiredMixin, View):
    template_name = "core/confirm_delete.html"

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, self.template_name, {"product": product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect("product-index")



#Papelera con borrado suave trabajar en otro momento
class ProductTrashView(View):
    template_name = "core/trash.html"

    def get(self, request):
        if not request.user.is_superuser:
            messages.error(request, "Acceso denegado.")
            return redirect("product-index")

        products = Product.objects.filter(deleted_at__isnull=False)
        return render(request, self.template_name, {"products": products})
    



# --------------------------------------------------------------------------------------------
# CLASS-BASED VIEWS(CBV) PARA CARRITO Y PEDIDOS
# --------------------------------------------------------------------------------------------

""" Buena práctica profesional: Atrapar la excepción, 
    registrar el error y mostrar un mensaje amigable al usuario"""
logger = logging.getLogger(name)

# --------------------------------------------------------------------------------------------
# Helper (global) - mantener como está
# --------------------------------------------------------------------------------------------
def get_or_create_active_cart(user):
    """
    Obtiene o crea un carrito activo (pendiente) para el usuario.
    Función global (no CBV) para mantener compatibilidad con otras partes.
    """
    if not user or not user.is_authenticated:
        raise ValueError("Se requiere un usuario autenticado para crear un carrito")

    # buscar "pendiente" sin importar mayúsculas/minúsculas
    status_pendiente = CartStatus.objects.filter(name__iexact="pendiente").first()

    # Si no existe, lo creamos (evitar get_or_create con __iexact)
    if not status_pendiente:
        try:
            status_pendiente = CartStatus.objects.create(
                name="pendiente",
                description="Carrito pendiente"
            )
        except Exception as e:
            logger.exception("Error creando CartStatus pendiente: %s", e)
            raise

    # Buscar carrito activo existente (sin borrar)
    cart = Cart.objects.filter(
        user=user,
        status=status_pendiente,
        deleted_at__isnull=True
    ).first()

    # Si no existe, crearlo
    if not cart:
        cart = Cart.objects.create(
            user=user,
            status=status_pendiente,
            quantity=0,
            price=0
        )

    return cart



# --------------------------------------------------------------------------------------------
# CATÁLOGO PÚBLICO (sin cambios funcionales)
# --------------------------------------------------------------------------------------------
def catalogo_view(request):
    """
    Vista pública del catálogo de productos.
    (Se mantiene como función para compatibilidad.)
    """
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    products = Product.objects.filter(deleted_at__isnull=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(categorynameicontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()


    context = {
        "page_obj": page_obj,
        "query": query,
        "categories": categories,
        "selected_category": category_id,
        "result_count": products.count()
    }
    return render(request, "core/catalogo.html", context)



# --------------------------------------------------------------------------------------------
#  CARRITO DE COMPRAS (CBV)
# --------------------------------------------------------------------------------------------
class CartView(LoginRequiredMixin, View):
    """
    GET: mostrar carrito actual del usuario.
    (Mantiene la lógica previa pero en CBV para estandarizar.)
    """
    template_name = "core/cart.html"

    def get(self, request, *args, **kwargs):
        try:
            cart = get_or_create_active_cart(request.user)
            cart_items = cart.cart_products.select_related('product').all()
            total = cart.get_total()
            total_quantity = cart.get_total_quantity()

            context = {
                "cart": cart,
                "cart_items": cart_items,
                "total": total,
                "total_quantity": total_quantity,
            }
            return render(request, self.template_name, context)
        
        except Exception as e:
            logger.exception("Error mostrando el carrito para user %s: %s", request.user, e)
            messages.error(request, "Ocurrió un error al cargar el carrito.")
            return redirect("catalogo")



class AddToCartView(LoginRequiredMixin, View):
    """
    POST: agrega producto al carrito. (Antes función add_to_cart)
    """
    def post(self, request, product_id, *args, **kwargs):
        try:
            product = get_object_or_404(Product, pk=product_id, deleted_at__isnull=True)
            quantity = int(request.POST.get("quantity", 1))

            if quantity <= 0:
                messages.error(request, "La cantidad debe ser mayor a 0.")
                return redirect("catalogo")

            cart = get_or_create_active_cart(request.user)

            # Si existe cart_product sumar cantidad, sino crearlo
            try:
                cart_product = CartProduct.objects.get(cart=cart, product=product)
                cart_product.quantity += quantity
                cart_product.save()
                messages.success(request, f"'{product.name}' agregado al carrito. Cantidad actualizada.")
            except CartProduct.DoesNotExist:
                CartProduct.objects.create(cart=cart, product=product, quantity=quantity)
                messages.success(request, f"'{product.name}' agregado al carrito.")

            # Recalcular totales (método en model)
            try:
                cart.calculate_total()
            except Exception:
                # No dejar que fallen los mensajes de UI
                logger.exception("Error recalculando totales del carrito id=%s", getattr(cart, 'id', None))

             # Redirigir de vuelta al catálogo para permitir seguir comprando
            return redirect("catalogo")
        
        except Exception as e:
            logger.exception("Error agregando producto al carrito: %s", e)
            messages.error(request, "No se pudo agregar el producto al carrito.")
            return redirect("catalogo")



class UpdateCartItemView(LoginRequiredMixin, View):
    """
    POST: actualizar cantidad de un item del carrito.
    """
    def post(self, request, item_id, *args, **kwargs):
        try:
            cart_item = get_object_or_404(CartProduct, pk=item_id, cart__user=request.user)
            quantity = int(request.POST.get("quantity", 1))

            if quantity <= 0:
                messages.error(request, "La cantidad debe ser mayor a 0.")
                return redirect("cart_view")

            cart_item.quantity = quantity
            cart_item.save()

            # Recalcular totales
            try:
                cart_item.cart.calculate_total()
            except Exception:
                logger.exception("Error recalculando totales tras update cart_item %s", cart_item.id)
                
            messages.success(request, "Cantidad actualizada.")
            return redirect("cart_view")

        except Exception as e:
            logger.exception("Error actualizando item del carrito: %s", e)
            messages.error(request, "No se pudo actualizar la cantidad del item.")
            return redirect("cart_view")



class RemoveFromCartView(LoginRequiredMixin, View):
    """
    POST: eliminar item del carrito.
    """
    def post(self, request, item_id, *args, **kwargs):
        try:
            cart_item = get_object_or_404(CartProduct, pk=item_id, cart__user=request.user)
            product_name = cart_item.product.name
            cart = cart_item.cart  # guardar referencia al carrito antes de eliminar

            cart_item.delete()

            # Recalcular totales
            try:
                cart.calculate_total()
            except Exception:
                logger.exception("Error recalculando totales tras eliminar cart_item")

            messages.success(request, f"'{product_name}' eliminado del carrito.")
            return redirect("cart_view")
        except Exception as e:
            logger.exception("Error eliminando item del carrito: %s", e)
            messages.error(request, "No se pudo eliminar el producto del carrito.")
            return redirect("cart_view")




# --------------------------------------------------------------------------------------------
#   ORDER / PEDIDO SECTION (CBV) SECCION PEDIDOS
# --------------------------------------------------------------------------------------------
class OrderCreateView(LoginRequiredMixin, View):
    """
    GET: mostrar formulario para crear pedido
    POST: procesar pedido (crear Delivery, Order, cambiar estado carrito)
    Mantiene la lógica principal, con iexact y cuidado en get/create.
    """
    template_name = "core/realizar_pedido.html"

    def get(self, request, *args, **kwargs):
        try:
            cart = get_or_create_active_cart(request.user)
            cart_items = cart.cart_products.all()

            if not cart_items.exists():
                messages.error(request, "Tu carrito está vacío. Agrega productos antes de realizar un pedido.")
                return redirect("cart_view")

            initial = {}
            if getattr(request.user, "address", None):
                initial["direccion"] = request.user.address

            form = PedidoForm(initial=initial)

            context = {
                "form": form,
                "cart": cart,
                "cart_items": cart_items,
                "total": cart.get_total(),
                "total_quantity": cart.get_total_quantity(),
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception("Error GET OrderCreateView: %s", e)
            messages.error(request, "Ocurrió un error al cargar la página de pedido.")
            return redirect("catalogo")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            cart = get_or_create_active_cart(request.user)
            cart_items = cart.cart_products.all()

            if not cart_items.exists():
                messages.error(request, "Tu carrito está vacío. Agrega productos antes de realizar un pedido.")
                return redirect("cart_view")

            form = PedidoForm(request.POST)
            if not form.is_valid():
                messages.error(request, "Por favor corrige los errores del formulario.")
                return render(request, self.template_name, {"form": form, "cart": cart, "cart_items": cart_items})

            data = form.cleaned_data
            metodo_pago = data["metodo_pago"]
            direccion = data["direccion"]

            # Comprobamos si el método de pago necesita comprobante (transferencia)
            metodo_pago_nombre = (metodo_pago.name or "").lower()
            es_transferencia = metodo_pago_nombre in ["transferencia", "transferencia bancaria", "pago movil", "pago móvil"]

            # Determinar tipo de pedido (usamos filter + create si no existe para evitar conflictos con seeders)
            tipo_pedido = None
            if es_transferencia:
                tipo_pedido = OrderType.objects.filter(name__iexact="comprobante de pago requerido").first()
                if not tipo_pedido:
                    tipo_pedido = OrderType.objects.create(
                        name="comprobante de pago requerido",
                        description="Pedido esperando comprobante de pago"
                    )
                mensaje_exito = "Pedido realizado exitosamente. Por favor, sube el comprobante de pago para que tu pedido pueda ser procesado."
            else:
                tipo_pedido = OrderType.objects.filter(name__iexact="pendiente").first()
                if not tipo_pedido:
                    tipo_pedido = OrderType.objects.create(
                        name="pendiente",
                        description="Pedido pendiente de aprobación"
                    )
                mensaje_exito = "Pedido realizado exitosamente. El administrador revisará tu pedido."

            # Estado completado para carrito (comprobamos con iexact)
            estado_completado = CartStatus.objects.filter(name__iexact="completado").first()
            if not estado_completado:
                estado_completado = CartStatus.objects.create(name="completado", description="Carrito completado")

            # Crear delivery
            entrega = Delivery.objects.create(user=request.user, secondary_address=direccion)

            # Actualizar carrito
            cart.status = estado_completado
            try:
                cart.calculate_total()
            except Exception:
                logger.exception("Error recalculando total al crear pedido para cart %s", getattr(cart, "id", None))
            cart.save()

            # Crear pedido
            pedido = Order.objects.create(
                user=request.user,
                cart=cart,
                order_type=tipo_pedido,
                payment_method=metodo_pago,
                delivery=entrega
            )

            messages.success(request, mensaje_exito)
            return redirect("detalle_pedido", order_id=pedido.id)

        except Exception as e:
            logger.exception("Error creando pedido: %s", e)
            messages.error(request, "Ocurrió un error al procesar el pedido. Intenta de nuevo.")
            return redirect("cart_view")


class UserOrdersView(LoginRequiredMixin, View):
    """
    Lista los pedidos del usuario autenticado (antes mis_pedidos).
    """
    template_name = "core/mis_pedidos.html"

    def get(self, request, *args, **kwargs):
        try:
            orders = Order.objects.filter(
                user=request.user,
                deleted_at__isnull=True
            ).select_related('order_type', 'payment_method', 'delivery', 'cart').prefetch_related('cartcart_productsproduct')

            paginator = Paginator(orders, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context = {"orders": page_obj, "page_obj": page_obj}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception("Error listando pedidos del usuario: %s", e)
            messages.error(request, "No se pudieron cargar tus pedidos.")
            return redirect("home")


class OrderDetailView(LoginRequiredMixin, View):
    """
    Muestra detalle de un pedido (antes detalle_pedido).
    """
    template_name = "core/detalle_pedido.html"

    def get(self, request, order_id, *args, **kwargs):
        try:
             """Vista para ver los detalles de un pedido específico"""
            order = get_object_or_404(Order, pk=order_id, user=request.user, deleted_at__isnull=True)

             # Obtener los items del carrito
            cart_items = order.get_cart_items()
            total = order.get_total()
            total_quantity = order.get_total_quantity()

             # Formulario para subir comprobante (si es necesario)
            if order.esperando_comprobante() and not order.tiene_comprobante():
                comprobante_form = ComprobantePagoForm(instance=order)

            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "total_quantity": total_quantity,
                "comprobante_form": comprobante_form,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception("Error mostrando detalle pedido %s: %s", order_id, e)
            messages.error(request, "No se pudo cargar el detalle del pedido.")
            return redirect("mis_pedidos")


class UploadReceiptView(LoginRequiredMixin, View):
    """
    Subir comprobante de pago (antes subir_comprobante).
    GET: mostrar form si aplica
    POST: procesar subida de comprobante y cambiar estado del pedido a 'pendiente'
    """
    template_name = "core/subir_comprobante.html"

    def get(self, request, order_id, *args, **kwargs):
        try:
            order = get_object_or_404(Order, pk=order_id, user=request.user, deleted_at__isnull=True)
            
             # Verificar que el pedido necesita comprobante y está esperando
            if not order.esperando_comprobante():
                messages.error(request, "Este pedido no requiere comprobante de pago.")
                return redirect("detalle_pedido", order_id=order_id)

            if order.tiene_comprobante():
                messages.info(request, "Este pedido ya tiene un comprobante de pago subido.")
                return redirect("detalle_pedido", order_id=order_id)

            form = ComprobantePagoForm(instance=order)
            return render(request, self.template_name, {"order": order, "form": form})
        except Exception as e:
            logger.exception("Error GET subir comprobante: %s", e)
            messages.error(request, "No se pudo abrir la pantalla de subida de comprobante.")
            return redirect("mis_pedidos")

    def post(self, request, order_id, *args, **kwargs):
        try:
            order = get_object_or_404(Order, pk=order_id, user=request.user, deleted_at__isnull=True)

            if not order.esperando_comprobante():
                messages.error(request, "Este pedido no requiere comprobante de pago.")
                return redirect("detalle_pedido", order_id=order_id)

            if order.tiene_comprobante():
                messages.info(request, "Este pedido ya tiene un comprobante de pago subido.")
                return redirect("detalle_pedido", order_id=order_id)

            if not request.FILES.get("comprobante_pago"):
                messages.error(request, "Debes seleccionar un archivo antes de subir el comprobante.")
                return redirect("detalle_pedido", order_id=order_id)

            form = ComprobantePagoForm(request.POST, request.FILES, instance=order)
            if form.is_valid():
                form.save()

                # Cambiar el estado del pedido a "pendiente"
                tipo_pendiente = OrderType.objects.filter(name__iexact="pendiente").first()
                if not tipo_pendiente:
                    tipo_pendiente = OrderType.objects.create(
                        name="pendiente",
                        description="Pedido pendiente de aprobación"
                    )

                order.order_type = tipo_pendiente
                # Guardar el comprobante
                order.save()

                messages.success(request, "Comprobante de pago subido exitosamente. Tu pedido está ahora pendiente de aprobación.")
                return redirect("detalle_pedido", order_id=order_id)
            else:
                messages.error(request, "Hubo un error al subir el comprobante. Por favor, verifica el archivo.")
                return render(request, self.template_name, {"order": order, "form": form})

        except Exception as e:
            logger.exception("Error POST subir comprobante: %s", e)
            messages.error(request, "Ocurrió un error al subir el comprobante.")
            return redirect("detalle_pedido", order_id=order_id)

