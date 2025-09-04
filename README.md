## 📘 README.md

# 🥐 Proyecto PanLyR

**PanLyR** es un emprendimiento dedicado a la creación de productos de panadería y repostería.  
Este sistema está siendo desarrollado con **Python**, **Django** y **PostgreSQL**, y tiene como objetivo gestionar productos, pedidos, stock y más funcionalidades relacionadas con el negocio.

---


### 📦 Estructura del Proyecto

El proyecto está dividido en tres apps principales, siguiendo buenas prácticas de organización:

| App           | Propósito                                                                 |
|---------------|---------------------------------------------------------------------------|
| auth_users   | Lógica de autenticación y modelo de usuario personalizado  
               |
| abcstracts    | Modelos abstractos reutilizables (fechas, borrado suave, etc.)  
          |
| core        | Lógica principal del negocio (productos, pedidos, interfaz de usuario)    |

---

### 🛠️ Avance actual

- ✅ Se creó el template de inicio (home.html) dentro de la app core, con diseño inicial.

- ✅ Se definió el modelo de usuario personalizado en auth_user/models.py.

- ✅ Se implementaron dos modelos abstractos en abcstracts/models.py:
  - TimeStampedModel: para manejar fechas de creación y actualización.
  - SoftDeleteModel: para implementar borrado lógico (no destructivo).

---

### 🚀 Tecnologías utilizadas

- Backend: Django 5.2.4
- Base de datos: PostgreSQL
- Frontend: HTML, CSS, Bootstrap (en proceso de integración)
- Control de versiones: Git + GitHub
- Gestión de entorno: python-decouple, dj-database-url

---

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
| Colab2         | Lógica de login (backend)          |
| Colab3         | Interfaz de login (frontend)       |
  
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
