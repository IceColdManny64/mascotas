# Spec: US03 — Ver Perfil Completo de Mascota

## User Story
"Como Adoptante Potencial, quiero poder ver el perfil completo de una mascota,
incluyendo su historial médico y requisitos especiales, antes de solicitar
la adopción."

## Descripción del Cambio
Página de detalle de mascota con toda su información. Muestra galería de fotos,
datos médicos, del refugio y acciones contextuales según el usuario.

## Contrato de Endpoint

### GET /pets/<id>
- Acceso: público (sin autenticación)
- Response 200: HTML con perfil completo
- Response 404: si pet no existe o is_active=False

Información mostrada:
Sección principal:

Galería de fotos (foto primaria destacada, resto navegables)
name, species, breed, age_years, size
temperament (badges visuales)
description

Sección compatibilidad:

children_friendly → badge verde "Apto con niños" / gris "No verificado"
other_animals_friendly → badge verde "Apto con otros animales"

Sección médica:

medical_history
special_requirements

Sección refugio:

Nombre del shelter (User.name)
User.city
Promedio de valoraciones del shelter (de US10)
Link al perfil del refugio /shelters/<shelter_id>

Sección acciones (condicional):

Botón "Solicitar adopción": visible si

usuario autenticado con role=adopter
pet.status='available'
no tiene AdoptionRequest existente para esta mascota


"Solicitud enviada": si ya tiene solicitud
Badge "Ya adoptado": si status='adopted'
Badge "Adopción en proceso": si status='pending'
Botón "Guardar favorita": si role=adopter autenticado
Botón "Editar": si role=shelter Y es dueño, o role=admin


## Reglas de Negocio
1. Perfil visible para todos sin login
2. status='adopted' → ocultar botón solicitud, mostrar badge
3. Adoptante con solicitud existente no ve botón (ve "Solicitud enviada")

## Tareas Atómicas
1. Implementar GET /pets/<id> en pets_bp
2. Query para verificar si adoptante actual ya tiene solicitud
3. Calcular promedio valoraciones del shelter
4. Crear template pets/detail.html con galería Bootstrap carousel
5. Renderizar badges de compatibilidad y status condicionalmente
6. Mostrar/ocultar botones según rol y estado

## Criterios de Aceptación
- [ ] Perfil accesible sin login, muestra todos los datos
- [ ] Galería de fotos funcional con foto primaria destacada
- [ ] Badges de compatibilidad visibles
- [ ] status='adopted' muestra badge y oculta botón solicitud
- [ ] Adoptante que ya solicitó ve "Solicitud enviada"
- [ ] Botón "Editar" solo visible al shelter dueño y admin
- [ ] Link al perfil del refugio funcional