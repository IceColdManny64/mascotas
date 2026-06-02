# Spec: US02 — Búsqueda y Filtrado de Mascotas

## User Story
"Como Adoptante Potencial, quiero poder buscar mascotas por especie, raza,
edad, tamaño, ubicación y compatibilidad para encontrar un compañero adecuado."

## Descripción del Cambio
Página principal de búsqueda con filtros combinables. Solo muestra mascotas
activas y disponibles. Resultados paginados con los filtros activos visibles.

## Decisiones de Arquitectura

### Búsqueda por ubicación
- **ELEGIDA: Filtro por city del shelter (string ILIKE)**
  - Razón: no requiere geolocalización, suficiente para el scope
- DESCARTADA: geolocalización con coordenadas
  - Razón: complejidad innecesaria para proyecto académico

### Paginación
- **ELEGIDA: Flask-SQLAlchemy .paginate() nativo**
  - Razón: integrado, simple, no requiere librería adicional

## Campos adicionales en Pet (delta de US01)
```python
# Estos campos ya están en US01, confirmar que están presentes:
children_friendly       Boolean, default=False
other_animals_friendly  Boolean, default=False
# Ubicación se obtiene via JOIN con User.city del shelter
```

## Contrato de Endpoint

### GET /pets
Query parameters (todos opcionales):
species               string, enum[dog,cat,rabbit,bird,other]
breed                 string, búsqueda parcial ILIKE '%valor%'
age_min               integer, min 0
age_max               integer, max 30
size                  string, enum[small,medium,large]
location              string, ILIKE sobre User.city del shelter
children_friendly     boolean (presencia del param = True)
other_animals_friendly boolean
page                  integer, default=1
Response 200: HTML con lista de mascotas y paginación
Filtros: AND entre todos los que estén presentes
Solo muestra: is_active=True AND status='available'
Orden: created_at DESC
Página size: 12 mascotas

## Reglas de Negocio
1. Sin filtros muestra todas las mascotas disponibles
2. Filtros son acumulativos (AND)
3. Búsqueda por breed es parcial case-insensitive
4. Ubicación busca sobre User.city del shelter dueño
5. Paginación mantiene todos los query params activos
6. Accesible sin autenticación

## Tareas Atómicas
1. Crear SearchForm en app/forms/pets.py (campos opcionales)
2. Implementar GET /pets en pets_bp con lógica de filtros encadenados
3. JOIN con User para filtrar por location
4. Implementar paginación con paginate(page, per_page=12)
5. Crear template pets/index.html con cards Bootstrap y formulario de filtros
6. Mantener filtros activos en el formulario tras búsqueda (pre-populate form)
7. Mostrar contador "X mascotas encontradas"
8. Mensaje vacío si no hay resultados

## Criterios de Aceptación
- [ ] Sin filtros muestra mascotas paginadas de 12 en 12
- [ ] Filtrar por species='dog' muestra solo perros
- [ ] Combinar species + size filtra correctamente (AND)
- [ ] breed='labra' encuentra mascotas con raza 'Labrador'
- [ ] Paginación página 2 mantiene filtros activos en URL
- [ ] Página muestra "X mascotas encontradas"
- [ ] Sin resultados muestra mensaje descriptivo
- [ ] Accesible sin login