## 📘 README.md

# 🥐 Proyecto PanLyR

**PanLyR** es un emprendimiento dedicado a la creación de productos de panadería y repostería.  
Este sistema está siendo desarrollado con **Python**, **Django** y **PostgreSQL**, y tiene como objetivo gestionar productos, pedidos, stock y más funcionalidades relacionadas con el negocio.

---

## 📦 Estado actual del proyecto

- El proyecto contiene únicamente la estructura inicial de Django.
- Incluye la carpeta `config/` con los archivos base (`settings.py`, `urls.py`, etc.).

- Se crearon 3 app (Etapa inicial):

- User_Auth: Para la lógica de usuario.

- Abstract: Para modelos abstractos y campos que se repiten (como nombre y descripción).

-Panlyr: Para la lógica principal de la aplicación (**Por ahora solo se ha trabajado en el borrador del templete de inicio de la aplicación en esta app**).

- Aún no se han definido modelos, vistas ni templates.
- Se recomienda **no ejecutar migraciones por ahora**, ya que no hay lógica de base de datos implementada.
- El archivo `.env.example` está disponible para configurar la conexión con PostgreSQL.

---

## 🔄 Actualizaciones futuras

Este proyecto se irá actualizando progresivamente con:

- Lógica de modelos (productos,clientes, pedidos)
- Templates y vistas
- Funcionalidades de stock, auditoría y gestión

---
