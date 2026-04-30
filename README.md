# 📋 Todo API - Backend

API REST construida con FastAPI y Python para gestionar tareas con autenticación de usuarios.

## 🚀 Tecnologías

- **FastAPI** — Framework web moderno y rápido
- **SQLAlchemy** — ORM para manejar la base de datos
- **SQLite** — Base de datos ligera
- **JWT** — Autenticación con tokens
- **Bcrypt** — Encriptación de contraseñas
- **Uvicorn** — Servidor ASGI

## ⚙️ Instalación

1. Clona el repositorio

git clone https://github.com/tu-usuario/todo-api.git
cd todo-api

2. Instala las dependencias

pip install fastapi[all] sqlalchemy python-jose passlib bcrypt

3. Arranca el servidor

uvicorn main:app --reload

4. Abre la documentación en tu navegador

http://localhost:8000/docs

## 📌 Endpoints

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | /Registrar | Crear cuenta | ❌ |
| POST | /Login | Iniciar sesión | ❌ |
| GET | /tareas | Obtener todas las tareas | ✅ |
| POST | /tareas | Crear tarea | ✅ |
| GET | /tareas/{id} | Obtener tarea por id | ✅ |
| PUT | /tareas/{id} | Actualizar tarea | ✅ |
| DELETE | /tareas/{id} | Eliminar tarea | ✅ |

## 🗂 Estructura del proyecto

todo-api/
├── main.py        # Rutas de la API
├── models.py      # Modelos de base de datos
├── database.py    # Configuración de SQLite
├── auth.py        # Lógica de autenticación JWT
└── tareas.db      # Base de datos (se genera automáticamente)

## 🔐 Autenticación

La API usa JWT (JSON Web Tokens). Para usar los endpoints protegidos:

1. Regístrate en `/Registrar`
2. Inicia sesión en `/Login` y copia el `access_token`
3. Envía el token en el header de cada petición:

Authorization: Bearer tu_token_aqui

## 👨‍💻 Autor

Mauro — [@tu-usuario-github](https://github.com/tu-usuario)
