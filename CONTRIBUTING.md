### 📘 `CONTRIBUTING.md` – Guía de colaboración para el proyecto PanLyR  
**Actualizado al 25 de septiembre de 2025**

---

## 🧁 Proyecto: PanLyR – Aplicación web para pedidos de panadería y repostería

Este documento describe la **metodología de trabajo**, el flujo de colaboración en **Git**, las **responsabilidades del equipo**, y las **tareas activas** para garantizar un desarrollo limpio, organizado y profesional.

---

## 🧭 Metodología de trabajo: Git con dos ramas

Usamos una metodología basada en **dos ramas principales**:

| Rama     | Propósito                                                                 |
|----------|---------------------------------------------------------------------------|
| `main`   | Código limpio, probado y listo para entrega o presentación                |
| `release`| Espacio para desarrollar y probar nuevas funcionalidades                  |

---

## ⚠️ Importante

**Nunca trabajes en la misma rama que otro colaborador al mismo tiempo.**  
Esto puede causar conflictos, sobrescritura de archivos o pérdida de trabajo.

Cada colaborador debe crear su propia rama desde `release` para trabajar de forma segura y ordenada.

---

## 👥 Roles del equipo

| Colaborador   | Rol principal                        | Rama sugerida     |
|---------------|--------------------------------------|-------------------|
| Kimberly      | Backend, modelos, estructura general | `models-core`     |
| Colaborador2  | Lógica de users (backend)            | `auth-login`      |
| Colaborador3  | Interfaz front-end (frontend)         | `auth-ui`         |

---

## 🛠️ Flujo de trabajo en Git

### 1. Crear una rama desde `release`

```bash
git checkout release
git checkout -b nombre-de-la-tarea
```

Ejemplo:

```bash
git checkout -b models-core
```

---

### 2. Trabajar localmente

- Realiza cambios en tu código.
- Haz commits con mensajes claros:

```bash
git add .
git commit -m "Agrega modelo Producto con campos básicos"
```

---

### 3. Subir la rama al repositorio

```bash
git push origin models-core
```

---

### 4. Crear un Pull Request (PR)

1. Ve al repositorio en GitHub.
2. Selecciona tu rama (ej. `models-core`).
3. Haz clic en **“Compare & Pull Request”**.
4. Asegúrate de que el PR se dirija a la rama `release`.
5. Escribe una descripción clara de lo que hiciste:
   - Qué funcionalidad agregaste
   - Qué archivos modificaste
   - Si hay algo pendiente por revisar
6. Espera revisión y aprobación por parte del equipo.

---

### 5. Fusionar el PR a `release`

- Una vez aprobado, se hace el merge.
- El código se integra sin afectar `main`.

---

### 6. Cuando todo esté probado, se fusiona `release` a `main`

```bash
git checkout main
git merge release
git push origin main
```

---

## 📋 Tareas activas del proyecto

Estas son las tareas asignadas actualmente por el profesor asesor:

- [x] Crear templates de login y registro
- [x] Definir modelos base en `abstracts`
- [x] Configurar estructura inicial del proyecto

🔧 **Tareas en desarrollo:**

- [ ] Implementar lógica de *soft delete* para evitar login de usuarios eliminados
- [ ] Crear CRUD completo para productos (crear, filtrar, actualizar, eliminar)
- [ ] Diseñar templates para productos y mejorar el `home.html` con:
  - Ciclo `for` que muestre productos destacados y nuevos desde la base de datos
  - Estilos con Bootstrap
- [ ] Personalizar el panel de administración con **Jazmín**
- [ ] Mostrar el total a pagar en el carrito según la tasa del día:
  - Moneda base: **peso colombiano (COP)**
  - Mostrar equivalencias en **USD** y **Bs. venezolanos**
  - Usar una API de tasa de cambio (ej. exchangerate.host)
  - Mostrar precios en COP (efectivo) y Bs (transferencia)

---

## 📦 Recomendaciones del profesor asesor

### App `abstracts`
- Crear modelos abstractos para campos comunes como `nombre`, `descripción`, `fecha_creación`.
- Usar `mixin.py` para definir *seeders* que poblen la base de datos con:
  - Categorías de productos
  - Formas de pago
  - Tipos de entrega

### App `auth_user`
- Implementar toda la lógica de login y autenticación.
- Crear vistas y formularios personalizados.

### App `core`
- Contendrá la lógica principal del negocio.
- Modelos de productos, pedidos, carrito, etc.
- Adaptar el diseño del `home.html` con colores cálidos (marrón, naranja, blanco).

---

## 🧠 Notas sobre precios y moneda

- Todos los precios se calculan en **COP**, ya que el emprendimiento compra ingredientes y calcula costos en esa moneda.
- El cliente verá el total a pagar en:
  - COP (efectivo)
  - Bs (transferencia)
  - USD (referencia)
- La conversión se hará en tiempo real usando la **tasa del día en dólares** como referencia.
- No es necesario agregar campos extra en el modelo, solo mostrar las conversiones en la vista y template.

---

## 🤝 ¿Tienes dudas?

Comunícate con Kimberly o revisa la guía `guia_instalacion.md` para configurar tu entorno correctamente.  
¡Gracias por colaborar en PanLyR! 🥖✨

---

### 📋 Buenas prácticas

- No hacer cambios directamente en main ni en release.
- Usar nombres de ramas en inglés y con guiones (auth-login, product_crud, etc.).
- Documentar cada funcionalidad en el README o en archivos separados.
- Validar que el código funcione antes de hacer Pull Request.
- Mantener comunicación constante entre colaboradores.

---