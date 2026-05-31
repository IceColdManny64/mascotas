# Spec: AUTH — Registro y Login de Usuarios

## Descripción
Feature base que deben existir antes que cualquier otra.
Tres roles: adopter, shelter, admin.

## Modelo de Datos

### User
```python
id            Integer, PK
email         String(150), unique, required
password_hash String(256), required
name          String(150), required
role          Enum['adopter','shelter','admin'], required
city          String(100), optional
phone         String(20), optional
bio           Text, optional
is_suspended  Boolean, default=False
suspended_at  DateTime, optional
created_at    DateTime UTC, auto
```

## Contratos de Endpoints

### GET /register
Response 200: formulario HTML

### POST /register
Request (form):
email     string, required, formato email válido, unique en DB
password  string, required, min 8 chars
name      string, required, max 150
role      string, required, enum[adopter, shelter]
city      string, optional
Response 302→/pets: éxito, login automático
Response 200: form con errores si email ya existe o validación falla
Nota: role=admin NO disponible en registro público

### GET /login
Response 200: formulario HTML

### POST /login
Request (form):
email     string, required
password  string, required
Response 302→next o /pets: éxito
Response 200: form con error "Credenciales inválidas" si falla
Response 200: form con error "Cuenta suspendida" si is_suspended=True

### GET /logout
- Requiere: login
- Response 302→/login

## Reglas de Negocio
1. Password hasheado con werkzeug generate_password_hash
2. Role=admin solo creado via script CLI o directamente en DB
3. is_suspended=True bloquea login con mensaje específico
4. Login automático tras registro exitoso

## Tareas Atómicas
1. Crear modelo User en app/models/user.py con Flask-Login UserMixin
2. Crear migración inicial
3. Crear RegisterForm y LoginForm en app/forms/auth.py
4. Crear blueprint auth_bp en app/routes/auth.py
5. Implementar GET/POST /register
6. Implementar GET/POST /login con check is_suspended
7. Implementar GET /logout
8. Configurar login_manager en app/extensions.py
9. Crear templates: auth/register.html, auth/login.html
10. Crear script seed_admin.py para crear usuario admin inicial

## Criterios de Aceptación
- [ ] Registro con email único crea usuario y hace login automático
- [ ] Registro con email duplicado muestra error inline
- [ ] Login con credenciales correctas redirige a /pets
- [ ] Login con credenciales incorrectas muestra "Credenciales inválidas"
- [ ] Usuario suspendido ve "Cuenta suspendida" en login
- [ ] Logout destruye sesión y redirige a /login
- [ ] role=admin no disponible en dropdown de registro