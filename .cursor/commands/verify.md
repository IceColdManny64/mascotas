# /verify — Validar implementación contra contrato

Cuando se ejecute este comando:
1. Lee la spec en /specs/features/<feature>.md
2. Verifica cada criterio de aceptación uno por uno
3. Para cada criterio: PASA o FALLA con explicación
4. Verifica que los endpoints respondan exactamente los códigos HTTP especificados
5. Verifica que las reglas de negocio estén implementadas
6. Genera reporte final: X/Y criterios cumplidos
7. Si hay fallos, listar exactamente qué corregir