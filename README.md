# Pet Adoption Platform

Plataforma de adopción de mascotas desarrollada con Spec-Driven Development (SDD).

## Stack
- Python 3.11 + Flask 3.x
- PostgreSQL 15
- Docker + docker-compose
- Bootstrap 5.3

## Metodología
Este proyecto usa SDD con OpenSpec. Toda feature comienza con una spec
en `.openspec/` antes de escribir código. Ver `.openspec/standards.md`
para las convenciones del proyecto.

## Comandos SDD disponibles en Cursor
- `/new` — genera propuesta formal desde user story
- `/apply` — implementa las tareas atómicas de una spec
- `/verify` — valida implementación contra criterios de aceptación
- `/archive` — mueve spec completada al historial

## Specs activas
Ver carpeta `.openspec/` — una spec por cada User Story.

## Orden de implementación
1. AUTH — registro y login (base de todo)
2. US01 — crear perfil de mascota
3. US02 + US03 — búsqueda y perfil completo
4. US04 + US05 — solicitudes de adopción
5. US06 — favoritos
6. US08 — mensajería
7. US07 — notificaciones
8. US10 — valoraciones
9. US09 — panel admin

## Levantar el proyecto
```bash
docker-compose up --build
```
La app estará en http://localhost:5000