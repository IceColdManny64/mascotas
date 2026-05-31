# Spec: US10 — Valoraciones de Refugios

## User Story
"Como Adoptante Potencial, quiero poder ver las valoraciones y comentarios de
otros usuarios sobre los refugios para tener más confianza en el proceso."

## Modelo de Datos

### Review
```python
id                  Integer, PK
shelter_id          FK → User.id, required
reviewer_id         FK → User.id, required
adoption_request_id FK → AdoptionRequest.id, required
rating              Integer, required, CHECK(1 <= rating <= 5)
comment             Text, optional
is_reported         Boolean, default=False
reported_reason     String(200), optional
created_at          DateTime UTC, auto
UNIQUE: (reviewer_id, shelter_id)
```

## Contratos de Endpoints

### GET /shelters/<id>
- Acceso: público
- Response 200: perfil del refugio
- Muestra:
User.name, User.city, User.bio
Promedio rating (avg redondeado a 1 decimal) y total valoraciones
Estrellas visuales Bootstrap
Lista de mascotas activas del shelter (paginada, 6 por página)
Lista de Reviews visibles (is_reported=False), más recientes primero
Formulario de valoración (solo si adoptante con adopción aprobada
de este shelter y sin review previa)
- Response 404: si user no existe o role != shelter

### POST /shelters/<id>/review
- Requiere: login + role=adopter
- Precondición: tiene AdoptionRequest approved para mascota de este shelter
- Request (form):
rating   integer, required, 1-5
comment  text, optional, max 500 chars
- Response 302→/shelters/<id>: éxito + flash
- Response 403: si no tiene adopción aprobada con ese shelter
- Response 400: si ya tiene review para ese shelter

### POST /reviews/<id>/report
- Requiere: login
- Efecto: Review.is_reported=True, Review.reported_reason=reason
- Response 302→/shelters/<shelter_id>: flash "Reportado para revisión"

## Reglas de Negocio
1. Solo adoptante con AdoptionRequest approved de mascota del shelter puede valorar
2. Una sola valoración por adoptante por shelter (UNIQUE)
3. Rating 1-5 enteros
4. Reviews con is_reported=True no se muestran en perfil público
5. Promedio recalculado en cada query (sin caché)

## Tareas Atómicas
1. Crear modelo Review en app/models/review.py
2. Crear migración
3. Crear ReviewForm en app/forms/reviews.py
4. Crear blueprint reviews_bp en app/routes/reviews.py
5. Implementar GET /shelters/<id> con cálculo de promedio y condicional de form
6. Implementar POST /shelters/<id>/review con verificación de permiso
7. Implementar POST /reviews/<id>/report
8. Crear templates: reviews/shelter_profile.html con estrellas Bootstrap
9. Registrar blueprint

## Criterios de Aceptación
- [ ] Adoptante con adopción aprobada ve formulario de valoración
- [ ] Adoptante sin adopción aprobada no ve el formulario
- [ ] Valoración aparece en perfil del shelter tras enviarla
- [ ] Promedio se actualiza correctamente
- [ ] Segunda valoración al mismo shelter retorna 400 con mensaje
- [ ] Valoración reportada desaparece del perfil público
- [ ] Admin puede eliminar valoraciones reportadas desde US09