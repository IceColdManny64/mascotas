# Spec: US04 — Enviar Solicitud de Adopción

## User Story
"Como Adoptante Potencial, quiero poder enviar una solicitud de adopción,
proporcionando información sobre mi hogar y mi experiencia con mascotas,
para iniciar el proceso."

## Modelo de Datos

### AdoptionRequest
```python
id              Integer, PK
pet_id          FK → Pet.id, required
adopter_id      FK → User.id, required
status          Enum['pending','approved','rejected'], default='pending'
home_type       Enum['house','apartment','farm'], required
has_yard        Boolean, required
other_pets      Boolean, required
other_pets_desc String(200), optional
has_children    Boolean, required
children_ages   String(100), optional
experience      Text, required
motivation      Text, required
created_at      DateTime UTC, auto
updated_at      DateTime UTC, auto-update
UNIQUE: (pet_id, adopter_id)
```

## Contratos de Endpoints

### GET /pets/<id>/apply
- Requiere: login + role=adopter
- Precondición: pet.status='available' y sin solicitud previa
- Response 200: formulario HTML
- Response 302→/pets/<id>: si ya tiene solicitud o mascota no disponible
- Response 403: si role=shelter o admin

### POST /pets/<id>/apply
Request (form):
home_type       string, required, enum[house,apartment,farm]
has_yard        boolean, required
other_pets      boolean, required
other_pets_desc string, optional, max 200
has_children    boolean, required
children_ages   string, optional, max 100
experience      text, required, min 50 chars
motivation      text, required, min 50 chars
Response 302→/adoptions/my: si éxito + flash "Solicitud enviada"
Response 200: formulario con errores si validación falla

### GET /adoptions/my
- Requiere: login + role=adopter
- Response 200: lista de AdoptionRequest del adoptante actual
- Muestra: nombre mascota, foto, status, fecha

## Reglas de Negocio
1. Solo role=adopter puede enviar solicitudes
2. Una solicitud por adoptante por mascota (UNIQUE constraint)
3. Solo para mascotas con status='available'
4. Al crear solicitud el status de Pet NO cambia
5. Al aprobar (US05): Pet.status='adopted', demás solicitudes→'rejected'

## Tareas Atómicas
1. Crear modelo AdoptionRequest en app/models/adoption.py
2. Crear migración
3. Crear AdoptionForm en app/forms/adoptions.py
4. Crear blueprint adoptions_bp en app/routes/adoptions.py
5. Implementar GET/POST /pets/<id>/apply con validaciones
6. Implementar GET /adoptions/my
7. Crear templates: adoptions/apply.html, adoptions/my.html
8. Registrar blueprint en app/__init__.py

## Criterios de Aceptación
- [ ] Adoptante autenticado accede a /pets/<id>/apply
- [ ] Formulario valida experience y motivation mínimo 50 chars
- [ ] Solicitud aparece en /adoptions/my con status 'pending'
- [ ] Segunda solicitud a misma mascota redirige con mensaje informativo
- [ ] Mascota con status!='available' no permite solicitar
- [ ] role=shelter recibe 403