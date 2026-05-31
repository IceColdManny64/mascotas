# Spec: US08 — Sistema de Mensajería Interna

## User Story
"Como Refugio/Propietario, quiero poder comunicarme con los adoptantes
potenciales a través de un sistema de mensajería dentro de la plataforma."

## Modelo de Datos

### Message
```python
id                  Integer, PK
sender_id           FK → User.id, required
receiver_id         FK → User.id, required
pet_id              FK → Pet.id, optional
adoption_request_id FK → AdoptionRequest.id, optional
content             Text, required, max 1000 chars
is_read             Boolean, default=False
created_at          DateTime UTC, auto
```

## Contratos de Endpoints

### GET /messages
- Requiere: login
- Response 200: bandeja de entrada con conversaciones agrupadas
- Agrupación: por pareja (sender_id, receiver_id) ordenado por último mensaje
- Muestra por conversación: nombre del otro usuario, preview 60 chars, fecha, badge no leídos

### GET /messages/<user_id>
- Requiere: login
- Response 200: conversación completa con ese usuario
- Orden: created_at ASC
- Efecto: marca como is_read=True todos los mensajes recibidos de user_id

### POST /messages/<user_id>
Request (form):
content   text, required, min 1, max 1000 chars
pet_id    integer, optional
Response 302→/messages/<user_id>: éxito
Response 200: formulario con error si content vacío o > 1000 chars

## Reglas de Negocio
1. Solo usuarios autenticados
2. Adoptante puede iniciar conversación desde perfil mascota o su solicitud
3. Shelter responde desde panel de solicitudes o mensajes
4. Al recibir mensaje: crear Notification tipo 'new_message'
5. Mensajes inmutables (no editar, no eliminar)
6. Máximo 1000 caracteres

## Tareas Atómicas
1. Crear modelo Message en app/models/message.py
2. Crear migración
3. Crear MessageForm en app/forms/messages.py
4. Crear blueprint messages_bp en app/routes/messages.py
5. Implementar GET /messages (bandeja agrupada)
6. Implementar GET /messages/<user_id> con mark as read
7. Implementar POST /messages/<user_id>
8. Crear Notification al enviar mensaje
9. Añadir badge mensajes no leídos en navbar (context processor)
10. Crear templates: messages/inbox.html, messages/conversation.html
11. Añadir botón "Enviar mensaje" en pets/detail.html

## Criterios de Aceptación
- [ ] Adoptante envía mensaje desde perfil de mascota
- [ ] Shelter ve el mensaje en su bandeja
- [ ] Shelter responde y adoptante recibe la respuesta
- [ ] Conversaciones agrupadas correctamente en bandeja
- [ ] Badge de no leídos visible en navbar
- [ ] Mensajes ordenados ASC (cronológicos) en conversación
- [ ] Más de 1000 chars muestra error de validación