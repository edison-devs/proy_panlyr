## 📘 README.md

# 🥐 Proyecto PanLyR

**PanLyR** es un emprendimiento dedicado a la creación de productos de panadería y repostería.  
Este sistema está siendo desarrollado con **Python**, **Django** y **MySQL**, y tiene como objetivo gestionar productos, pedidos y más funcionalidades relacionadas con el negocio.

---


### 📦 Estructura del Proyecto

El proyecto está dividido en tres apps principales, siguiendo buenas prácticas de organización:

| App           | Propósito                                                                 |
|---------------|---------------------------------------------------------------------------|
| auth_user   | Lógica de autenticación y modelo de usuario personalizado                 |
| abstract    | Modelos abstractos reutilizables (fechas, borrado suave, etc.)            |
| core        | Lógica principal del negocio (productos, pedidos, interfaz de usuario)    |

---


📘 Gestión de Roles, Permisos y Datos Iniciales (Seeders)

🧩 Estructura general

El sistema utiliza una serie de comandos personalizados de Django (management commands) para crear automáticamente:

-Usuarios base (como el usuario root),

-Roles o grupos de usuario (admin, employed, viewer),

-Permisos especiales (incluyendo los de Soft Delete),
Y datos iniciales de las tablas descriptivas como categorías, métodos de pago y estados del sistema.


-Estos comandos se encuentran en la app abstracts dentro de la carpeta:

abstracts/management/commands/


---

⚙️ Seeders principales

1️⃣ seed_root_user.py

Crea el usuario root (superusuario) con credenciales:

usuario: root
contraseña: root123
correo: root@panlyr.com

Además, si ya existe el grupo “Admin”, lo asocia automáticamente a este usuario.

> 💡 Este se ejecuta solo una vez. Si el usuario ya existe, el sistema lo omite.




---

2️⃣ seeders.py

Es el archivo principal que ejecuta todos los seeders en orden:

-python manage.py seeders

Dentro llama a otros seeders:

-seeders_categories

-seeders_permissions

-seeders_groups

-seeder_user


Esto asegura que el sistema tenga todos los datos base antes de iniciar desarrollo o pruebas.


---

3️⃣ seeders_categories.py

Crea los datos iniciales de:

Categorías (Panadería, Repostería, Galletas)

Métodos de pago (Efectivo, Transferencia)

Estados del carrito y del pedido

Estados de entrega


> ✅ Este seeder solo crea los datos si no existen, evitando duplicados.




---

4️⃣ seed_groups.py

Crea los grupos predeterminados del sistema:

Grupo Descripción Permisos

admin Control total del sistema Todos los permisos
employed Operaciones básicas (productos, pedidos, carritos) CRUD limitado
viewer Solo visualización view_


> 💡 Este sistema de grupos permite una estructura clara para administrar usuarios con diferentes niveles de acceso.




---

5️⃣ seed_softdelete_permissions.py

Crea permisos especiales para todos los modelos que hereden de SoftDeleteMixin.
Agrega automáticamente permisos:

soft_delete_modelo

restore_modelo


> ⚙️ Esto facilita un sistema de “borrado suave”, donde los registros no se eliminan realmente de la base de datos, sino que se marcan como inactivos.




---

🧱 Gestión de grupos en templates

Archivo:
abstracts/templates_tags/groups.py

Permite usar filtros en los templates HTML de Django para verificar el rol del usuario:

{% if user|has_group:"admin" %}
   <p>Bienvenido, administrador</p>
{% endif %}

También incluye funciones como:

has_any_group → verifica si pertenece a uno de varios grupos.

get_groups → obtiene todos los grupos del usuario autenticado.



---

📍 Ubicación de archivos estáticos

Todos los archivos static (CSS, JS, imágenes) se manejan en la app:

core/static/

De esta manera se centralizan los recursos visuales del proyecto.


---

---

# 🧁 — Panel Administrativo por Vistas

Este documento explica la nueva estructura base del panel administrativo que reemplaza el panel de Django. El objetivo es mantener un entorno simple, limpio y completamente en español, ideal para continuar el desarrollo de la lógica de pedidos y gestión de productos.

---

## 🧩 Estructura General del Proyecto

El sistema ahora se organiza de forma modular, utilizando Bootstrap 5 y vistas personalizadas.

### 📂 core/templates/sidebar/
Carpeta principal del panel administrativo.

| Archivo / Carpeta | Descripción |
|--------------------|-------------|
| index.html | Vista principal (dashboard de bienvenida). |
| grupos.html | Gestión de roles o grupos de usuario. |
| pedidos.html | Módulo inicial para pedidos. |
| reportes.html | Módulo de reportes y estadísticas. |
| user.html | Vista para gestión de usuarios. |
| products/ | CRUD de productos: index.html, create.html, update.html. |
| category_products/ | CRUD de categorías de producto: index.html, create.html. |

---

## 🧱 Base de la Interfaz: base_simple.html

Archivo principal que define la estructura base del sitio y que heredan todas las vistas del panel.  
Incluye integración con Bootstrap 5.3.3, bloques personalizables y carga dinámica de contenido.


- 📌 También se añadió una carpeta en core/static con Bootstrap local para pruebas sin conexión.


---


---

👥 Manejo de Roles

-Los roles serán gestionados manualmente desde las vistas, sin el panel Django.

-Esto permitirá un flujo más controlado, totalmente personalizable y 100% en español.


Roles definidos:

-admin → Acceso completo al panel.

-employee → Gestión de productos y pedidos.

-viewer → Solo lectura.

sin rol (cliente) → Acceso restringido al panel, solo puede realizar pedidos desde la parte pública.


> 🔐 El sistema validará el rol antes de permitir el acceso a cada vista.



⚙️ Cambios Principales en esta Versión

🧩 1. Refactorización del Módulo core/models.py

Se eliminaron los modelos relacionados con inventario (entradas y salidas) y se reestructuró el módulo para enfocarse únicamente en la gestión de productos, carritos, pedidos, entregas y pagos.


✅ Nuevos modelos activos

Modelo Descripción

-Category Clasifica los productos (panes, tortas, galletas, etc.).

-Product Define productos con imagen, precio, descripción y categoría.

-Cart / CartProduct / CartStatus Manejan el carrito de compras y sus estados.

-Order / OrderType Representan los pedidos realizados por los usuarios.

-Payment / PaymentMethod Registran los métodos y montos de pago.

-Delivery / DeliveryStatus Administran la información de entrega del cliente.


🧠 Buenas prácticas aplicadas:

-on_delete=models.PROTECT → evita el borrado accidental de datos con relaciones.

-SoftDeleteMixin y TimestampedMixin → agregan borrado suave y seguimiento temporal al admin django.

-Eliminación del campo role en el modelo User, reemplazado por el sistema nativo de permisos y grupos de Django.

-Código modular y fácil de escalar.



---

🧭 2. Actualización del Módulo core/views.py

El módulo views se simplificó para trabajar sin inventario, incorporando un CRUD limpio para productos, una vista centralizada de dashboard y lógica inicial para el flujo de pedidos.

🔑 Principales vistas:

-render_home → redirige a la página principal.

-dashboard → nuevo panel administrativo unificado.

-ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView → CRUD completo de productos con paginación y manejo de mensajes.

-ProductTrashView → muestra los productos eliminados mediante soft delete.

-realizar_pedido → lógica en desarrollo para que usuarios autenticados generen pedidos.


💡 Detalles técnicos:

Estructura basada en Class-Based Views.

Manejo de errores y mensajes con django.contrib.messages.

Paginación con Paginator.

Separación clara entre lógica y presentación (templates).



---

🧰 3. Cambios en core/forms.py

Se simplificaron los formularios al eliminar toda lógica relacionada con stock o control de existencias.

📋 Formularios activos:

-ProductForm → Permite crear y editar productos.

-Campos: category, name, price, description, image.

-Uso de widgets personalizados para mantener coherencia visual con Bootstrap.


-PedidoForm → Gestiona el proceso de pedido del cliente.

-Campos: producto, cantidad, metodo_pago, tipo_pedido, direccion.

-Integración con modelos PaymentMethod y OrderType.


---


🎨 4. Estructura de Templates (core/templates/partials/)

Se añadió una carpeta partials para componentes reutilizables que mejoran la organización y mantenibilidad del frontend.

---

🚧 Estado Actual del Proyecto


- ✅ Base visual y estructural completa.
- ✅ Rutas configuradas y plantillas enlazadas.
- ⚙️ En desarrollo: lógica de roles y permisos.
- 🛒 Próximo paso: implementar la lógica de pedidos (carrito, registro y gestión básica).



---



### 🛠️ Avance Anterior

- ✅ Se usó Bootstrap para lograr un diseño responsivo en todos los paneles.

- ✅ Se creó el archivo styles1.css con comentarios por sección para facilitar mantenimiento.

⚠️ Recomendación: mantener un solo archivo de estilos para rendimiento, pero bien comentado.

- ✅ Se creó la carpeta includes/ dentro de core/templates para reutilizar fragmentos de código.

📌 ¿Qué es un include? Es una forma de insertar un bloque HTML en múltiples templates sin duplicar código.

- ✅ Se creó la carpeta admin/ dentro de core/templates y core/static para personalizar el panel de Django.



---

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


[x] Bootstrap integrado en templates

[x] Archivo único de estilos comentado (styles1.css)

[x] Includes para reutilización de código

[x] Personalización visual del Django Admin

[x] Borrado suave en modelo User

[x] Íconos personalizados en el admin

[x] Base de datos migrada a MySQL


🧁 Cosas por hacer

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


---

### Bootstrap

Este proyecto usa Bootstrap de forma local para desarrollo sin conexión.  
Los archivos locales están ignorados en `.gitignore`.  
Para producción o colaboración, se recomienda usar el CDN:

html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>



##Nota:

-Cualquier duda sobre como clonar el proyecto ver el archivo **guia_instalacion.md**

-Para dudas en la metodologia de trabajo con git ver **CONTRIBUTING.md**

