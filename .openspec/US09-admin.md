# Spec: US09 — Panel de Administración y Moderación

## User Story
"Como Administrador, quiero poder moderar los perfiles de mascotas y los
usuarios para asegurar la calidad de la información y la seguridad."

## Campos adicionales en modelos existentes (deltas)
```python
# Ya definidos en standards/US01: Pet.is_active Boolean default=True
# Agregar a User:
User.is_suspended  Boolean, default=False
User.suspended_at  DateTime, optional
```

## Contratos de Endpoints

### GET /admin
- Requiere: role=admin
- Response 200: dashboard HTML
- Métricas:
total_pets, available_pets, adopted_pets
total_users_adopter, total_users_shelter
pending_requests (global)
new_pets_30d, new_users_30d

### GET /admin/pets
- Response 200: tabla paginada, todas las mascotas, con filtro por status/is_active

### POST /admin/pets/<id>/deactivate
- Efecto: Pet.is_active = False
- Response 302→/admin/pets + flash

### POST /admin/pets/<id>/activate
- Efecto: Pet.is_active = True
- Response 302→/admin/pets + flash

### GET /admin/users
- Response 200: tabla paginada, todos los usuarios, con rol y estado

### POST /admin/users/<id>/suspend
- Precondición: id != current_user.id
- Efecto: User.is_suspended=True, User.suspended_at=now()
- Response 302→/admin/users + flash
- Response 400: si intenta suspenderse a sí mismo

### POST /admin/users/<id>/unsuspend
- Efecto: User.is_suspended=False, User.suspended_at=None
- Response 302→/admin/users + flash

### GET /admin/reviews
- Response 200: tabla de Review con is_reported=True

### POST /admin/reviews/<id>/delete
- Efecto: DELETE físico del Review
- Response 302→/admin/reviews + flash

## Reglas de Negocio
1. Solo role=admin accede a /admin/*
2. Mascota con is_active=False no aparece en /pets ni búsquedas
3. Usuario con is_suspended=True: flash "Cuenta suspendida" en login y no puede entrar
4. Admin no puede suspenderse a sí mismo

## Tareas Atómicas
1. Crear blueprint admin_bp en app/routes/admin.py con decorador role check
2. Implementar dashboard con métricas SQL
3. Implementar listado y toggle is_active de mascotas
4. Implementar listado y toggle is_suspended de usuarios
5. Implementar check en login: si is_suspended → flash + no login
6. Implementar listado y delete de reviews reportadas
7. Crear templates: admin/dashboard.html, admin/pets.html, admin/users.html, admin/reviews.html

## Criterios de Aceptación
- [ ] Dashboard muestra métricas correctas
- [ ] Desactivar mascota la oculta del listado público
- [ ] Suspender usuario impide su login con mensaje claro
- [ ] Admin no puede suspenderse a sí mismo (botón deshabilitado o 400)
- [ ] role=adopter o shelter reciben 403 en /admin
- [ ] Admin puede eliminar valoraciones reportadas