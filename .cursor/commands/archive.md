# /archive — Archivar spec completada

Cuando se ejecute este comando con una feature verificada:

1. Mueve .openspec/<feature>.md a .openspec/archive/<feature>.md
2. Si no existe .openspec/archive/, créala primero
3. Actualiza o crea .openspec/archive/INDEX.md con:
   - Nombre de la feature archivada
   - Fecha de completación
   - Lista de criterios que pasaron
   - Decisiones de arquitectura clave tomadas
4. Confirmar que el archivo fue movido correctamente