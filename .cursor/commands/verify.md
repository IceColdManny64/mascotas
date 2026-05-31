# /verify — Validar implementación contra contrato

Cuando se ejecute este comando:

1. Lee la spec activa en .openspec/ indicada
2. Lee .openspec/standards.md para verificar convenciones
3. Verifica cada criterio de aceptación uno por uno
4. Para cada criterio reporta: PASA ✓ o FALLA ✗ con explicación concreta
5. Verifica que los endpoints existen y respetan los códigos HTTP de la spec
6. Verifica que las reglas de negocio están implementadas en el código
7. Verifica que los modelos tienen todos los campos definidos en la spec
8. Genera reporte final: X/Y criterios cumplidos
9. Si hay fallos, listar exactamente qué archivo y qué línea corregir