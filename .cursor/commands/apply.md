# /apply — Ejecutar tareas de la spec

Cuando se ejecute este comando apuntando a una spec:

1. Lee el archivo de spec indicado en .openspec/
2. Lee .openspec/standards.md para respetar arquitectura y convenciones
3. Antes de empezar: actualiza PROGRESS.md marcando la feature como
   🟡 En progreso con tu nombre de sesión y fecha actual
4. Ejecuta CADA tarea atómica en el orden listado en la spec
5. Por cada tarea: escribe el código y confirma que no hay errores de sintaxis
6. Respeta exactamente los contratos de endpoint definidos en la spec
7. Respeta exactamente los modelos de datos definidos en la spec
8. No inventar campos, rutas ni comportamientos no especificados
9. No modificar specs ya archivadas en .openspec/archive/
10. Al terminar todas las tareas: reportar qué se completó y qué tuvo problemas