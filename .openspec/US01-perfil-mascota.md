# Spec: US01 — Crear Perfil de Mascota

## User Story
"Como Refugio/Propietario, quiero poder crear un perfil detallado para cada
mascota disponible en adopción, incluyendo fotos, descripción, especie, raza,
edad y temperamento, para atraer a posibles adoptantes."

## Descripción del Cambio
Un usuario autenticado con rol `shelter` puede registrar nuevas mascotas en la
plataforma. Cada mascota tiene información básica, médica y fotos. La mascota
queda disponible inmediatamente tras su creación.

## Decisiones de Arquitectura

### Almacenamiento de fotos
- **ELEGIDA: Carpeta local /app/static/uploads/** con nombre UUID
  - Razón: sin dependencias externas, suficiente para el scope del proyecto
- DESCARTADA: Cloudinary/S3
  - Razón: requiere credenciales externas y aumenta complejidad innecesariamente

### Relación fotos
- **ELEGIDA: Tabla separada PetPhoto con FK a Pet**
  - Razón: permite múltiples fotos, marcar primaria, eliminar individualmente
- DESCARTADA: campo JSON de URLs en Pet
  - Razón: dificulta queries y no permite metadatos por foto

## Modelos de Datos

### Modelo Pet
```pythonid                    Integer, PK, autoincrement
name                  String(100), required
species               Enum['dog','cat','rabbit','bird','other'], required
breed                 String(100), optional
age_years             Integer, optional
size                  Enum['small','medium','large'], optional
temperament           String(200), optional
description           Text, required
medical_history       Text, optional
special_requirements  Text, optional
children_friendly     Boolean, default=False
other_animals_friendly Boolean, default=False
status                Enum['available','pending','adopted'], default='available'
is_active             Boolean, default=True
shelter_id            FK → User.id, not null
created_at            DateTime UTC, auto
updated_at            DateTime UTC, auto-update

### Modelo PetPhoto
```pythonid          Integer, PK
pet_id      FK → Pet.id, cascade delete
url         String(300), required
is_primary  Boolean, default=False

## Contrato de Endpoints

### GET /pets/new
- Requiere: login + role=shelter
- Response 200: formulario HTML de creación
- Response 302: redirect /login si no autenticado
- Response 403: si role != shelter

### POST /pets/new
Request (multipart/form-data):name          string, required, max 100
species       string, required, enum[dog,cat,rabbit,bird,other]
breed         string, optional, max 100
age_years     integer, optional, min 0, max 30
size          string, optional, enum[small,medium,large]
temperament   string, optional, max 200
description   string, required
medical_history       string, optional
special_requirements  string, optional
children_friendly     boolean
other_animals_friendly boolean
photos        file[], min 1, max 5, extensiones [jpg,jpeg,png,webp], max 2MB c/u
Response 302: redirect /pets/<id> si éxito
Response 200: formulario con errores inline si validación falla

### GET /pets/<id>/edit
- Requiere: login + (role=shelter AND pet.shelter_id=current_user.id) OR role=admin
- Response 200: formulario pre-poblado
- Response 403: si no tiene permiso
- Response 404: si pet no existe o is_active=False

### POST /pets/<id>/edit
- Mismo request que POST /pets/new (fotos opcionales en edición)
- Response 302: redirect /pets/<id> si éxito

### POST /pets/<id>/delete
- Requiere: mismo permiso que edit
- Regla: falla si hay AdoptionRequest con status='pending'
- Response 302: redirect /pets si éxito
- Response 400 + mensaje flash: si hay solicitudes pendientes

## Reglas de Negocio
1. Solo role=shelter puede crear mascotas
2. status se asigna 'available' automáticamente al crear
3. Primera foto subida tiene is_primary=True
4. No eliminar mascota con solicitudes en status='pending'
5. shelter_id = current_user.id (asignado en servidor, no en form)
6. Mascota con is_active=False no aparece en búsquedas públicas

## Tareas Atómicas
1. Crear modelos Pet y PetPhoto en app/models/pet.py con relaciones
2. Crear migración con flask db migrate
3. Crear PetForm en app/forms/pets.py con validaciones WTForms
4. Crear blueprint pets_bp en app/routes/pets.py
5. Implementar GET/POST /pets/new con manejo de fotos
6. Implementar GET/POST /pets/<id>/edit
7. Implementar POST /pets/<id>/delete con verificación de solicitudes
8. Crear templates: pets/new.html, pets/edit.html con Bootstrap 5
9. Registrar blueprint en app/__init__.py

## Criterios de Aceptación
- [ ] Shelter autenticado accede a /pets/new sin error
- [ ] Formulario muestra errores inline si falta nombre o descripción
- [ ] Mascota creada aparece en listado con status 'available'
- [ ] Primera foto se muestra como imagen principal en card
- [ ] Usuario con role=adopter recibe 403
- [ ] Usuario no autenticado es redirigido a /login
- [ ] Intentar eliminar mascota con solicitudes pendientes muestra flash error
- [ ] Edición pre-puebla todos los campos correctamente