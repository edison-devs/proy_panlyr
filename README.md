## 📘 README.md

# 🥐 Proyecto PanLyR

**PanLyR** es un emprendimiento dedicado a la creación de productos de panadería y repostería.  
Este sistema está siendo desarrollado con **Python**, **Django** y **MySQL**, y tiene como objetivo gestionar productos, pedidos, stock y más funcionalidades relacionadas con el negocio.

---


### 📦 Estructura del Proyecto

El proyecto está dividido en tres apps principales, siguiendo buenas prácticas de organización:

| App           | Propósito                                                                 |
|---------------|---------------------------------------------------------------------------|
| auth_user   | Lógica de autenticación y modelo de usuario personalizado                 |
| abstract    | Modelos abstractos reutilizables (fechas, borrado suave, etc.)            |
| core        | Lógica principal del negocio (productos, pedidos, interfaz de usuario)    |

---

### 🛠️ Avance actual

- ✅ El login redirige correctamente al panel según el rol del usuario (superadmin, admin, cliente) con una implementación temporal.

- ✅ Se usó Bootstrap para lograr un diseño responsivo en todos los paneles.

- ✅ Se creó el archivo styles1.css con comentarios por sección para facilitar mantenimiento.

⚠️ Recomendación: mantener un solo archivo de estilos para rendimiento, pero bien comentado.

- ✅ Se creó la carpeta includes/ dentro de core/templates para reutilizar fragmentos de código.

📌 ¿Qué es un include? Es una forma de insertar un bloque HTML en múltiples templates sin duplicar código.

- ✅ Se creó la carpeta admin/ dentro de core/templates y core/static para personalizar el panel de Django.

- ✅ Se creó un logout.html en templates/admin/ para forzar redirección al login personalizado al cerrar sesión desde el admin (🔧 aún no funcional).

- ✅ Se creó la carpeta placeholders/ en core/templates con HTMLs genéricos para probar redirecciones y lógica futura (reportes, pedidos, papelera, carrito).

- ✅ El panel de usuario se muestra según el rol, con diseño profesional y accesos personalizados.

- ✅ El panel de Django ya tiene íconos personalizados y estilos adaptados.

- ✅ El modelo User permite elegir el rol desde el admin y ya maneja borrado suave.


### 

---

## ⚙️ Actualización del Modelo de Usuario (Roles funcionales)

📌 Objetivo:  
Corregir el problema de que los roles no se asignaban correctamente al crear un usuario desde consola o el panel de administración.

### 🔧 Cambios realizados
- Se actualizó el método save() del modelo User en auth_users/models.py.
- Esta actualización sincroniza automáticamente los flags internos de Django (is_staff, is_superuser) con el campo role.

### 📁 Ubicación del cambio
Ruta del archivo:

proy_panlyr/auth_users/models.py


🧠 Explicación

Si el usuario tiene rol superadmin, obtiene permisos de súper usuario (is_superuser=True).

Si tiene rol admin, puede acceder al panel de administración (is_staff=True).

Si es cliente, no tiene permisos de staff ni de súper usuario.


⚠️ Nota:
Esta implementación es provisional, creada para pruebas rápidas del sistema y colaboración entre el equipo.
En una versión futura se reemplazará por una lógica más segura basada en signals o managers personalizados.

🧾 Verificación

1. Crear un usuario desde consola:

python manage.py createsuperuser


2. Revisar la base de datos:

Tabla: users

Campo: role

El nuevo usuario debería tener asignado su rol correctamente según la lógica anterior.



3. Probar acceso al panel:

superadmin → Acceso total

admin → Solo panel intermedio

cliente → Panel de cliente


---

✅ Resultado esperado:
Los roles ahora se asignan correctamente y permiten redirigir al panel correspondiente sin necesidad de configuraciones adicionales en el admin de Django.


---


### 🛠️ Avance anterior

- ✅ Se creó el template de inicio (home.html) dentro de la app core, con diseño inicial.

- ✅ Se definió el modelo de usuario personalizado en auth_user/models.py.

- ✅ Se implementaron dos modelos abstractos en abcstracts/models.py:
  - TimeStampedModel: para manejar fechas de creación y actualización.
  - SoftDeleteModel: para implementar borrado lógico (no destructivo).

- ✅ Se añadio la libreria jazmin al setting para configurar los estilos del admin de django

- ✅ Ruta del admin cambiada

- ✅ Se hizo un crud base con estilos basicos USA BOOTSTRAP ya esta enlazado al view.py **falta configurar los botones para que el login reconozca los roles de los usuarios**

---


✅ Checklist de tareas completadas

[x] Redirección por rol desde el login

[x] Paneles personalizados por tipo de usuario

[x] Bootstrap integrado en templates

[x] Archivo único de estilos comentado (styles1.css)

[x] Includes para reutilización de código

[x] Personalización visual del Django Admin

[x] Borrado suave en modelo User

[x] Íconos personalizados en el admin

[x] Base de datos migrada a MySQL


🧁 Cosas por hacer

[ ] Investigar cómo redirigir correctamente desde el Django Admin al login personalizado (logout.html)

[ ] Desarrollar lógica de borrado suave para productos

[ ] Implementar lógica de pedidos (crear, listar, cancelar)

[ ] Desarrollar lógica del carrito (agregar, eliminar, confirmar)

[ ] Estilizar el Django Admin con la paleta de colores de PanLyR

[ ] Crear lógica para desactivar permisos según el rol (checkbox dinámico en el admin)


📌 Prioridades sugeridas

🛒 Lógica del carrito (flujo de compra)

📦 Lógica de pedidos (gestión y visualización)

🧹 Borrado suave para productos

🎨 Estilizar el Django Admin con colores PanLyR



---

📝 Actualización de Formularios (Login & Register)

📌 Cambios realizados

1. **Actualización de forms.py** en la app auth_users:
Se añadieron widgets con la clase form-control en los campos (username, email, password, etc.).

- Esto fue necesario porque, al usar Django, cuando se renderizan los formularios automáticamente con {{ form.as_p }} o {{ form }}, los inputs HTML generados no traen las clases de Bootstrap.

- Sin la clase form-control, los inputs no se muestran con el estilo visual de Bootstrap (bordes redondeados, colores de focus, etc.).

- Con form-control aplicado desde los widgets, aseguramos que los formularios se vean consistentes con el resto del diseño.


Ejemplo:

username = forms.CharField(
    label="Nombre de Usuario",
    max_length=150,
    widget=forms.TextInput(attrs={
        'placeholder': 'Define nombre de usuario',
        'class': 'form-control'
    })
)


2. **Creación de una carpeta templates/ global en el proyecto**

Dentro se añadió el archivo:

templates/partials/form_field.html

Este archivo permite controlar de forma centralizada el estilo de los campos de formulario, evitando duplicar código en cada app.


Ejemplo de uso en un template:

{% include "partials/form_field.html" with field=form.username %}

Código del archivo form_field.html:

{# partials/form_field.html
   Renderiza un campo de formulario con su label y mensaje de error.
   Uso recomendado: {% include 'partials/form_field.html' with field=form.username %}
#}

<div class="mb-3">
  {{ field.label_tag }}
  {{ field }}
  {% if field.errors %}
    <div class="form-text text-danger small">{{ field.errors.0 }}</div>
  {% endif %}
</div>



🎯 Propósito de esta implementación

- Mantener la consistencia visual entre formularios de Login y Register usando Bootstrap.

- Evitar que Django modifique los estilos al renderizar los inputs.

- Facilitar la colaboración en equipo, centralizando la lógica de estilos en un único archivo (form_field.html) en lugar de replicarlo en cada app.

- Mejorar la mantenibilidad: cualquier cambio de estilo en los formularios se hace en un solo lugar.

---

## 🗂️ Administración con Borrado Suave (Soft Delete)

Este proyecto implementa un sistema de borrado suave para proteger los datos y permitir restauraciones desde el panel de administración. A continuación se detallan los componentes clave y cómo se aplican:

### 🔧 Mixins utilizados
- `SoftDeleteMixin`: agrega el campo `deleted_at` y métodos `.soft_delete()` y `.restore()` a los modelos.
- `TimestampedMixin`: agrega `created_at` y `updated_at` con etiquetas en español.
- `SoftDeleteAdminMixin`: añade acciones de borrado suave, restauración y borrado definitivo al panel de Django.
- `DeletedAtFilterMixin`: permite filtrar visualmente entre registros borrados y activos.

### 🧑‍💻 Cómo se aplica en el admin
- Los modelos que usan `SoftDeleteMixin` deben heredar `SoftDeleteAdminMixin` en su clase `ModelAdmin`.
- Se recomienda mostrar `deleted_at` en `list_display` y en `readonly_fields`.
- Se puede usar `get_queryset()` para mostrar solo los registros activos por defecto.
- Las acciones disponibles en el panel son:
  - `Borrado suave de seleccionados`
  - `Restaurar seleccionados`
  - `Borrado definitivo de seleccionados`

### 🔒 Seguridad en el modelo User
- El campo `_is_active` controla si el usuario puede iniciar sesión.
- La propiedad `is_active` combina `_is_active` y `deleted_at` para bloquear el acceso si el usuario fue eliminado suavemente.

### 🎨 Visualización
- Se pueden mostrar íconos o etiquetas como “🗑️ Eliminado”, “✅ Activo”, “⛔ Inactivo” en el panel para mayor claridad.

### 📁 Archivos relevantes
- `abcstracts/models.py` → Mixins de borrado y timestamps
- `abcstracts/mixin.py` → Acciones y filtros para el admin
- `core/admin.py` → Aplicación de los mixins en modelos de negocio
- `auth_users/admin.py` → Configuración avanzada del modelo `User`

---


### 🚀 Tecnologías utilizadas


- Backend: Django 5.2.4
- Base de datos: MySQL
- Frontend: HTML, CSS, Bootstrap (en proceso de integración)
- Control de versiones: Git + GitHub
- Gestión de entorno: python-decouple, dj-database-url

---

### Se agregaron los Modelos al admin.py en app core y auth_users

### 📂 Instalación del proyecto

1. Clonar el repositorio:
  
   git clone https://github.com/usuario/panlyr.git
   
2. Crear entorno virtual:
  
   python -m venv env
  
   env\Scripts\activate     # En Windows
   
3. Instalar dependencias:
  
   pip install -r requirements.txt
   
4. Configurar variables de entorno:
   - Renombrar env.example a .env
   - Completar los valores necesarios (SECRET_KEY, DATABASE_URL, etc.)

---

### 👥 Equipo de desarrollo

| Nombre         | Rol principal                      |
|----------------|------------------------------------|
| Kim (Colab1) | Backend, modelos, estructura del proyecto |
| Colab2         | Lógica de pedidos  (backend)          |
| Colab3         | Interfaz de las templates (frontend)       |
  
---

### ⚠️ Nota importante sobre colaboración

> No se debe trabajar en la misma rama al mismo tiempo.  
Cada colaborador debe crear su propia rama realese/nombre-de-la-tarea para evitar conflictos y pérdida de trabajo. Los cambios se integran mediante Pull Requests hacia la rama release, donde se revisan antes de fusionarse a main.

---


### 🐍 Versión recomendada de Python

- El proyecto funciona con Python 3.10 o superior.  
 
- Usa entornos virtuales para evitar conflictos.

### 🐘 Versión recomendada de PostgreSQL

- El proyecto funciona con PostgreSQL 16 o 17.  
- Se recomienda usar la versión más estable disponible en tu equipo.  
- Evita usar funciones exclusivas de PostgreSQL 17 para mantener compatibilidad.

### 📌 Próximos pasos

- Implementar lógica completa de login en auth_user.

- Crear seeders en abcstracts/mixin.py para poblar:
  - Categorías de productos
  - Formas de pago
  - Tipos de entrega

- Desarrollar modelos de productos y pedidos en core.

- Integrar Bootstrap para mejorar la interfaz visual.

---

### Bootstrap

Este proyecto usa Bootstrap de forma local para desarrollo sin conexión.  
Los archivos locales están ignorados en `.gitignore`.  
Para producción o colaboración, se recomienda usar el CDN:

html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>



## 🔄 Actualizaciones futuras

Este proyecto se irá actualizando progresivamente con:

- Lógica de modelos (productos,clientes, pedidos)
- Templates y vistas
- Funcionalidades de stock, auditoría y gestión

---

##Nota:

-Cualquier duda sobre como clonar el proyecto ver el archivo **guia_instalacion.md**

-Para dudas en la metodologia de trabajo con git ver **CONTRIBUTING.md**

