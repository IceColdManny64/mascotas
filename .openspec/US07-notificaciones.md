# Spec: US07 — Notificaciones de Nuevas Mascotas

## User Story
"Como Adoptante Potencial, quiero recibir notificaciones cuando nuevas mascotas
que coinciden con mis criterios de búsqueda estén disponibles."

## Modelos de Datos

### SearchAlert
```python
id          Integer, PK
adopter_id  FK → User.id, required
species     Enum['dog','cat','rabbit','bird','other'], optional
breed       String(100), optional
age_max     Integer, optional
size        Enum['small','medium','large'], optional
children_friendly     Boolean, optional
other_animals_friendly Boolean, optional
is_active   Boolean, default=True
created_at  DateTime UTC, auto
```

### Notification
```python
id          Integer, PK
user_id     FK → User.id, required
type        Enum['new_pet_match','request_approved','request_rejected','new_message']
message     String(300), required
link        String(200), optional
is_read     Boolean, default=False
created_at  DateTime UTC, auto
```

## Contratos de Endpoints

### GET /alerts
- Requiere: login + role=adopter
- Response 200: lista de alertas activas del adoptante

### POST /alerts
Request (form):
species               string, optional
breed                 string, optional, max 100
age_max               integer, optional
size                  string, optional
children_friendly     boolean
other_animals_friendly boolean
Response 302→/alerts: éxito + flash
Response 400: si ya tiene 3 alertas activas

### POST /alerts/<id>/delete
- Requiere: ser dueño de la alerta
- Response 302→/alerts

### GET /notifications
- Requiere: login
- Response 200: lista de notificaciones del usuario, más recientes primero

### POST /notifications/mark-read
- Requiere: login
- Efecto: todos los Notification del usuario → is_read=True
- Response 302→/notifications

## Reglas de Negocio
1. Al crear mascota nueva (US01 POST /pets/new):
   - Evaluar TODAS las SearchAlert activas en DB
   - Para cada alerta que coincida: crear Notification para ese adoptante
   - Coincidencia: todos los campos no-None de la alerta deben cumplirse (AND)
2. Badge en navbar = COUNT de Notification is_read=False del usuario actual
3. Máximo 3 alertas activas por usuario (no crear la 4a)
4. No crear notificaciones duplicadas (misma mascota + mismo adopter)

## Tareas Atómicas
1. Crear modelos SearchAlert y Notification en app/models/message.py
2. Crear migración
3. Crear AlertForm en app/forms/alerts.py
4. Crear blueprint alerts_bp en app/routes/alerts.py
5. Implementar CRUD de alertas
6. Crear función check_alerts(pet) llamada desde POST /pets/new
7. Implementar GET /notifications y POST /notifications/mark-read
8. Añadir badge de notificaciones en base.html (query en context processor)
9. Crear templates: alerts/index.html, notifications/index.html

## Criterios de Aceptación
- [ ] Adoptante crea alerta con criterios parciales
- [ ] Al crear mascota que coincide, se genera Notification
- [ ] Badge en navbar muestra número correcto de no leídas
- [ ] Marcar como leído pone badge a 0
- [ ] No se crean duplicados para la misma mascota y adoptante
- [ ] No se puede crear 4a alerta (flash error)