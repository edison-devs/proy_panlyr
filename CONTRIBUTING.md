## 📘 CONTRIBUTING.md – Guía de colaboración para el proyecto PanLyR

### 🧁 Proyecto: PanLyR – Aplicación web para pedidos de panadería y repostería

Este documento describe la **metodología de trabajo**,flujo de colaboración en **Git**, y responsabilidades del **equipo** para garantizar un desarrollo limpio, organizado y profesional.

---

### 🧭 Metodología de trabajo: Git con dos ramas

Usaremos una metodología sencilla basadados **ramas principales**:

| Rama        | Propósito                                                                 |
|-------------|---------------------------------------------------------------------------|
| main      | Código limpio, probado y listo para entrega o presentación  
              |
| release   | Espacio para desarrollar y probar nuevas funcionalidades                  |

---

### ⚠️ Advertencia importante Nunca trabajes en la misma rama que otro colaborador** al mismo tiempo**  

Esto puede causar conflictos de código sobrescritura de archivos**pérdida de trabajo**.

Cada colaborador debe crear su propia rama desde release para trabajar de forma segura y ordenada.

---

### 👥 Roles del equipo

| Colaboración     |           Rol principal            |sugerida                  
|-----------------|------------------------------------|----Colaborador1 **(Kim)** | Backend, modelos, estructura del proyecto          

| Colaborador2         | Lógica de login (backend)   
                
| Colaborador3         | Interfaz de login (frontend)
---


### 🛠️ Flujo de trabajo en Git

#### 1. Crear una rama desde release

git checkout release
git checkout -b nombre-de-la-tarea
Ejemplo:

git checkout -b models-core
#### 2. Trabajar localmente

- Realiza cambios en tu código.
- Haz commits con mensajes claros:

git add .
git commit -m "Agrega modelo Producto con campos básicos"
#### 3. Subir la rama al repositorio

git push origin models-core
#### 4. Crear un Pull Request (PR)

- Ve a GitHub.
- Selecciona tu rama (models-core, por ejemplo).
- Haz clic**“Compare & Pull Request"**.
- Asegúrate de que el PR se dirija a la rama release.
- Escribe una descripción clara de lo que hiciste.
- Espera revisión y aprobación por parte del equipo.

#### 5. Fusionar el PR a release

- Una vez aprobado, se hace el merge.
- El código se integra sin afectar main.

#### 6. Cuando todo esté probado, se fusiona release a main

git checkout main
git merge release
git push origin main
---

### 📦 Recomendaciones del profesor asesor

1. **App abstract**:
   - Crear modelos abstractos para campos comunes como nombre, descripción, fecha_creación.
   - Usar mixin.py para definir *seeders* que poblen la base de datos con:
     - Categorías de productos
     - Formas de pago
     - Tipos de entrega,etc

2. **App auth_user**:
   - Implementar toda la lógica de login y autenticación.
   - Crear vistas y formularios personalizados.
   
3. **App core**:
   - Contendrá la lógica principal del negocio.
   - Modelos de productos, pedidos, carrito, etc.
   - Adaptar el diseño del home.html con colores cálidos (marrón, naranja, blanco).

---

### 📋 Buenas prácticas

- No hacer cambios directamente en main ni en release.
- Usar nombres de ramas en inglés y con guiones (auth-login, product-crud, etc.).
- Documentar cada funcionalidad en el README o en archivos separados.
- Validar que el código funcione antes de hacer Pull Request.
- Mantener comunicación constante entre colaboradores.

---