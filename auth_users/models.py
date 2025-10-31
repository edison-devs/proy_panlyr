from django.db import models
from django.contrib.auth.models import AbstractUser
from abcstracts.models import TimestampedMixin, SoftDeleteMixin


class User(AbstractUser, TimestampedMixin, SoftDeleteMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ciudad')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='País')

    USERNAME_FIELD = 'username'  # Ya viene de AbstractUser
    REQUIRED_FIELDS = ['email']  # Se mantiene como campo obligatorio

    is_staff = models.BooleanField(
        default=False,
        verbose_name="¿Puede entrar al administrador?"
    )

    is_superuser = models.BooleanField(
        default=False,
        verbose_name="¿Es súper Usuario?"
    )

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

# ✅ Flujo esperado
# 1-Creas un usuario → puede iniciar sesión.

# 2-Le haces borrado suave desde el admin → deleted_at se llena → ya no puede iniciar sesión.

# 3-Lo restauras → deleted_at vuelve a None → puede iniciar sesión otra vez.

# 4-Si lo marcas como inactivo (_is_active=False) → tampoco podrá iniciar sesión aunque no esté borrado