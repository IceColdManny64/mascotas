# Spec: US06 — Guardar Mascotas como Favoritas

## User Story
"Como Adoptante Potencial, quiero poder guardar mascotas como favoritas para
acceder a ellas fácilmente más tarde y comparar opciones."

## Modelo de Datos

### Favorite
```python
id          Integer, PK
adopter_id  FK → User.id, required
pet_id      FK → Pet.id, required
created_at  DateTime UTC, auto
UNIQUE: (adopter_id, pet_id)
```

## Contratos de Endpoints

### POST /pets/<id>/favorite
- Requiere: login + role=adopter
- Comportamiento toggle:
  * Si NO existe → INSERT → response {"status":"added"}
  * Si existe → DELETE → response {"status":"removed"}
- Response 200: JSON {"status": "added"|"removed"}
- Response 401: si no autenticado → JSON {"redirect": "/login"}
- Response 403: si role=shelter

### GET /adoptions/favorites
- Requiere: login + role=adopter
- Response 200: HTML lista de mascotas favoritas
- Muestra: foto, nombre, species, status actual, botón quitar

## Reglas de Negocio
1. Solo role=adopter puede usar favoritos
2. Máximo 50 favoritos por usuario
3. Mostrar status actual de cada mascota en la lista
4. El endpoint POST retorna JSON para actualizar UI sin reload

## Tareas Atómicas
1. Crear modelo Favorite en app/models/adoption.py
2. Crear migración
3. Implementar POST /pets/<id>/favorite con lógica toggle en adoptions_bp
4. Implementar GET /adoptions/favorites
5. Crear template adoptions/favorites.html
6. Añadir botón corazón en pets/detail.html con JS fetch para toggle
7. JS: cambiar ícono corazón lleno/vacío según response

## Criterios de Aceptación
- [ ] Clic en corazón en perfil agrega a favoritos sin reload de página
- [ ] Segundo clic quita de favoritos
- [ ] Mascota aparece en /adoptions/favorites tras agregarla
- [ ] Status actual de mascota visible en lista de favoritos
- [ ] Sin login, clic en corazón retorna JSON con redirect a login
- [ ] No se puede agregar más de 50 favoritos (error con flash)