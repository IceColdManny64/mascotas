# /archive — Archivar spec completada

Cuando se ejecute este comando con una feature verificada:

1. Mueve .openspec/<feature>.md a .openspec/archive/<feature>.md
2. Si no existe .openspec/archive/, créala primero
3. Actualiza o crea .openspec/archive/INDEX.md con:
   - Nombre de la feature archivada
   - Fecha de completación
   - Lista de criterios que pasaron
   - Decisiones de arquitectura clave tomadas
4. Actualiza PROGRESS.md:
   - Cambia el estado de la feature a 🟢 Completa
   - Registra la fecha en la columna Notas
   - Revisa si alguna feature que dependía de esta puede cambiar a disponible
5. Confirmar que todos los archivos fueron actualizados correctamente