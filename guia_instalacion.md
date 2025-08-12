# 🧁 Guía de Instalación del Proyecto PanLyR

Pasos para instalar y preparar el entorno de desarrollo del proyecto PanLyR.

---

## 📥 Clonar el repositorio

bash
git clone https://github.com/TuUsuario/proy_panlyr.git
cd proy_panlyr

---

## 🐍 Crear y activar el entorno virtual

### 🔹 Crear el entorno:

bash
python -m venv venv

### 🔹 Activar el entorno:

- **Git Bash**:

  
bash
  soCMDnv/Scripts/activate
 

- **CMD**:

  
cmd
 PowerShellactivate.bat
 

- **PowerShell**:

  
powershell
  venv\Scripts\Activate.ps1
 

---

## 📦 Instalar dependencias

bash
pip install -r requirements.txt

---

## 🔐 Configurar el archivo `.env`

bash
cp .env.example .env

Luego edita el archivo `.env` con tus credenciales de PostgreSQL.

---

## 💬 Créditos

Guía creada por **Kimberly**  
En colaboración con **Copilot**
---