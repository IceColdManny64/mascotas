# /apply — Ejecutar tareas de la spec

Cuando se ejecute este comando con una spec aprobada:
1. Lee el archivo de spec indicado en /specs/features/
2. Ejecuta CADA tarea atómica en el orden listado
3. Por cada tarea: escribe el código, confirma que compila/ejecuta
4. Respeta exactamente los contratos de endpoint definidos
5. Respeta exactamente los modelos de datos definidos
6. No inventar campos, rutas o comportamientos no especificados
7. Al terminar, reportar qué tareas se completaron y cuáles fallaron