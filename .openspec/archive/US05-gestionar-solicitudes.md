# Spec: US05 — Gestionar Solicitudes de Adopción

## User Story
"Como Refugio/Propietario, quiero poder gestionar las solicitudes de adopción,
revisarlas, aceptarlas o rechazarlas, y comunicarme con los solicitantes."

## Contratos de Endpoints

### GET /shelter/requests
- Requiere: login + role=shelter
- Response 200: lista de todas las AdoptionRequest de las mascotas del shelter
- Agrupa o filtra por status
- Muestra: nombre mascota, nombre adoptante, fecha, status con color

### GET /shelter/requests/<id>
- Requiere: login + role=shelter + ser dueño de la mascota de la solicitud
- Response 200: detalle completo de la solicitud
- Response 403: si la solicitud es de una mascota de otro shelter
- Response 404: si no existe

Información mostrada:

Foto y nombre de la mascota
Todos los campos del AdoptionRequest
Nombre, ciudad, bio del adoptante
Fecha de envío y último update
Historial de mensajes vinculados (pet_id + users)
Botones Aprobar/Rechazar (solo si status='pending')


### POST /shelter/requests/<id>/approve
- Requiere: mismo permiso que GET detail
- Precondición: status='pending'
- Efecto:
  1. AdoptionRequest.status = 'approved'
  2. Pet.status = 'adopted'
  3. Todas las demás AdoptionRequest de ese pet → status='rejected'
  4. Crear Notification tipo 'request_approved' para adoptante aprobado
  5. Crear Notification tipo 'request_rejected' para adoptantes rechazados
- Response 302→/shelter/requests: con flash "Adopción aprobada"
- Response 400: si status != 'pending'

### POST /shelter/requests/<id>/reject
- Efecto:
  1. AdoptionRequest.status = 'rejected'
  2. Crear Notification tipo 'request_rejected' para el adoptante
- Response 302→/shelter/requests/<id>: con flash "Solicitud rechazada"

## Reglas de Negocio
1. Shelter solo ve solicitudes de SUS mascotas
2. No se puede modificar solicitud ya aprobada o rechazada
3. Aprobar una solicitud rechaza automáticamente todas las demás del mismo pet
4. Al aprobar, Pet.status cambia a 'adopted'

## Tareas Atómicas
1. Implementar GET /shelter/requests en adoptions_bp
2. Implementar GET /shelter/requests/<id>
3. Implementar POST /shelter/requests/<id>/approve con transacción DB
4. Implementar POST /shelter/requests/<id>/reject
5. Crear templates: adoptions/shelter_list.html, adoptions/shelter_detail.html
6. Crear Notification records en el approve/reject

## Criterios de Aceptación
- [ ] Shelter ve solo sus propias solicitudes
- [ ] Lista distingue pending/approved/rejected con colores Bootstrap
- [ ] Al aprobar: pet.status='adopted', demás solicitudes='rejected'
- [ ] Botones aprobar/rechazar no visibles en solicitudes ya procesadas
- [ ] role=adopter recibe 403 al acceder a /shelter/requests