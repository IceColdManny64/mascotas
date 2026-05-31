# /new — Generar propuesta desde User Story

Cuando se ejecute este comando con una user story:

1. Lee la user story proporcionada y todos los archivos existentes en .openspec/
2. Lee .openspec/standards.md para entender la arquitectura del proyecto
3. Genera un documento de propuesta formal en .openspec/<nombre-feature>.md
4. El documento debe contener:
   - Descripción del cambio desde perspectiva de negocio
   - Modelos de datos afectados con todos sus campos y tipos
   - Contratos de endpoints (request/response exactos con códigos HTTP y JSON)
   - Decisiones de arquitectura con alternativas descartadas y su razón
   - Requerimientos no funcionales
   - Lista de tareas atómicas numeradas y verificables
   - Criterios de aceptación binarios (se cumple o no se cumple)
5. NO escribir código todavía
6. Mostrar la propuesta completa y preguntar si se aprueba antes de continuar