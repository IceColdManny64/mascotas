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

## Orden de implementación (completado)

Ver `PROGRESS.md` y `.openspec/archive/INDEX.md` para el historial.

## Levantar el proyecto
```bash
docker compose up --build
```
La app estará en http://localhost:5000

**Admin por defecto:** `admin@mascotas.local` / `admin12345`