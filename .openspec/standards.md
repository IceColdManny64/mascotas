# Pet Adoption Platform — Project Standards

## 1. Stack Tecnológico
- Backend: Python 3.11 con Flask 3.x
- ORM: SQLAlchemy 2.x con Flask-SQLAlchemy
- Migraciones: Flask-Migrate (Alembic)
- Autenticación: Flask-Login + Werkzeug password hashing
- Formularios: Flask-WTF + WTForms
- Base de datos: PostgreSQL 15
- Frontend: Jinja2 templates + Bootstrap 5.3
- Contenedor: Docker + docker-compose
- Servidor desarrollo: Flask built-in (debug=True)

## 2. Estructura de Carpetas
pet-adoption/
├── app/
│   ├── init.py          ← Application factory (create_app)
│   ├── extensions.py        ← db, login_manager, migrate
│   ├── models/
│   │   ├── init.py
│   │   ├── user.py
│   │   ├── pet.py
│   │   ├── adoption.py
│   │   ├── message.py
│   │   └── review.py
│   ├── routes/
│   │   ├── init.py
│   │   ├── auth.py          ← /register, /login, /logout
│   │   ├── pets.py          ← /pets/*
│   │   ├── adoptions.py     ← /adoptions/, /shelter/
│   │   ├── messages.py      ← /messages/*
│   │   ├── alerts.py        ← /alerts/*
│   │   ├── reviews.py       ← /shelters/, /reviews/
│   │   └── admin.py         ← /admin/*
│   ├── forms/
│   │   └── *.py             ← WTForms por módulo
│   ├── templates/
│   │   ├── base.html        ← layout con navbar y notif badge
│   │   └── */               ← subcarpetas por módulo
│   └── static/
│       ├── css/
│       └── uploads/         ← fotos de mascotas
├── migrations/
├── .openspec/
│   ├── standards.md         ← este archivo
│   └── *.md                 ← specs activas
├── .openspec/archive/       ← specs completadas
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

## 3. Convenciones de Código
- Clases: PascalCase (User, AdoptionRequest, PetPhoto)
- Funciones y variables: snake_case
- Blueprints: nombre del módulo en minúsculas (auth_bp, pets_bp)
- Constantes: UPPER_SNAKE_CASE
- Archivos: snake_case.py

## 4. Modelos SQLAlchemy
- Toda tabla tiene: id (Integer PK autoincrement), created_at (DateTime UTC auto)
- Relaciones: usar back_populates, no backref
- Enums: usar Python Enum class + SQLAlchemy Enum type
- Soft delete: usar is_active boolean en lugar de DELETE físico

## 5. Rutas Flask
- Blueprints con url_prefix definido en registro
- Decoradores de autorización: @login_required, @roles_required('shelter')
- Flash messages para feedback al usuario
- Redirecciones post-POST siempre (PRG pattern)
- Errores: abort(403) para no autorizado, abort(404) para no encontrado

## 6. Roles de Usuario
- adopter: buscar mascotas, solicitar adopción, favoritos, mensajes, valorar
- shelter: crear/editar mascotas, gestionar solicitudes, mensajes
- admin: moderar todo el contenido y usuarios

## 7. Seguridad
- Passwords: werkzeug.security generate_password_hash / check_password_hash
- CSRF: Flask-WTF en todos los formularios POST
- Archivos subidos: validar extensión y tamaño máximo 2MB

## 8. Docker
- Un servicio 'web' (Flask) y un servicio 'db' (PostgreSQL)
- Volume mount para hot-reload en desarrollo
- Variables de entorno via docker-compose environment