# Specs archivadas

| Feature | Fecha | Criterios cumplidos | Decisiones clave |
|---------|-------|---------------------|------------------|
| AUTH | 2026-06-01 | 7/7 | Admin solo por seed; passwords con werkzeug |
| US01 | 2026-06-01 | 8/8 | Fotos en static/uploads UUID; PetPhoto tabla separada |
| US02 | 2026-06-01 | 8/8 | Filtro ubicación por city del shelter; paginate 12 |
| US03 | 2026-06-01 | 7/7 | Perfil público; acciones por rol/estado |
| US04 | 2026-06-01 | 6/6 | UNIQUE (pet_id, adopter_id) |
| US05 | 2026-06-01 | 5/5 | Approve transaccional + notificaciones |
| US06 | 2026-06-01 | 6/6 | Toggle JSON favoritos máx 50 |
| US07 | 2026-06-01 | 6/6 | Modelos tempranos; check_alerts en POST /pets/new |
| US08 | 2026-06-01 | 7/7 | Mensajes inmutables; badge navbar |
| US09 | 2026-06-01 | 6/6 | Soft delete mascotas is_active |
| US10 | 2026-06-01 | 7/7 | UNIQUE reviewer+shelter; reviews reportadas ocultas |

## Orden de implementación ejecutado

Fase 0 → AUTH → US01 → US07 (modelos) → US02 → US03 → US07 (UI) → US04 → US06 → US05 → US08 → US10 → US09
