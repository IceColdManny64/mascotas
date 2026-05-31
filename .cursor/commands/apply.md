# /apply — Ejecutar tareas de la spec

Cuando se ejecute este comando apuntando a una spec:

1. Lee el archivo de spec indicado en .openspec/
2. Lee .openspec/standards.md para respetar arquitectura y convenciones
3. Ejecuta CADA tarea atómica en el orden listado en la spec
4. Por cada tarea: escribe el código y confirma que no hay errores de sintaxis
5. Respeta exactamente los contratos de endpoint definidos en la spec
6. Respeta exactamente los modelos de datos definidos en la spec
7. No inventar campos, rutas ni comportamientos no especificados
8. No modificar specs ya archivadas en .openspec/archive/
9. Al terminar, reportar qué tareas se completaron y cuáles tuvieron problemas