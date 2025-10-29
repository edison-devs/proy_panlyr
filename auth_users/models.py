from django.db import models
from django.contrib.auth.models import AbstractUser
from abcstracts.models import TimestampedMixin, SoftDeleteMixin


class User(AbstractUser, TimestampedMixin, SoftDeleteMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ciudad')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='País')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    is_staff = models.BooleanField(
        default=False,
        verbose_name="¿Es administrador?"
    )
    
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="¿Es súper administrador?"
    )

    ROLE_CHOICES = [
        ('superadmin', 'Super Administrador'),
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')

    def is_superadmin(self):
        return self.role == 'superadmin'

    def is_admin(self):
        return self.role == 'admin'

    def is_cliente(self):
        return self.role == 'cliente'

    # Campo real editable en el admin
    _is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")

    @property
    def is_active(self):
        """
        Un usuario solo puede iniciar sesión si:
        - No está eliminado (deleted_at es None)
        - Y está marcado como activo (_is_active=True)
        """
        return self.deleted_at is None and self._is_active

    class Meta:
        db_table = "users"
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def str(self):
        return f"{self.username} ({self.email})"

    # 🚧 Lógica temporal para sincronizar banderas internas con el rol del usuario
    # ------------------------------------------------------------
    # Esta parte del código es provisional.
    # Por ahora ayuda a mantener consistencia entre los campos:
    #   - role
    #   - is_superuser
    #   - is_staff
    #
    # 🔸 La asignación automática del rol inicial se hace desde signals.py
    # 🔸 Este método solo asegura que al modificar el rol manualmente, las banderas se actualicen también.
    # 🔸 Más adelante se reemplazará por una implementación más limpia.
    # ------------------------------------------------------------
    def save(self, *args, **kwargs):
        # Mantiene sincronización entre role y flags de Django
        """
        Manejo temporal de roles para pruebas.
        - Si el usuario es superusuario, el rol será 'superadmin'.
        - Si no es superusuario pero es staff, el rol será 'admin'.
        - En los demás casos, el rol será 'cliente'.
        """
        if self.is_superuser:
            self.role = 'superadmin'
            self.is_staff = True
        elif self.is_staff:
            self.role = 'admin'
        else:
            self.role = 'cliente'

        super().save(*args, **kwargs)



# ✅ Flujo esperado
# 1-Creas un usuario → puede iniciar sesión.

# 2-Le haces borrado suave desde el admin → deleted_at se llena → ya no puede iniciar sesión.

# 3-Lo restauras → deleted_at vuelve a None → puede iniciar sesión otra vez.

# 4-Si lo marcas como inactivo (_is_active=False) → tampoco podrá iniciar sesión aunque no esté borrado