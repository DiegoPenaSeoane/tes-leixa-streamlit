# INFORME DE AMPLIACIÓN — TES Leixa v805 ampliado desde v804

## Resumen ejecutivo

Se ha generado un paquete ampliado respetando la estructura lógica del paquete v804 y sin tocar usuarios, contraseñas, progreso, login, guardado ni lógica de Streamlit.

- Preguntas originales v804: 3413
- Preguntas nuevas añadidas v805: 180
- Total preguntas en banco ampliado: 3593
- IDs duplicados tras ampliación: 0
- Respuestas correctas inválidas tras ampliación: 0

## Distribución de preguntas nuevas

| Módulo | Preguntas nuevas |
|---|---:|
| MP0053 Logística sanitaria | 60 |
| MP0059 Planes de emergencias | 60 |
| MP0061 Anatomofisiología | 60 |


## Enfoque docente de la ampliación

Las preguntas nuevas se han diseñado para reforzar:

- Diferencias entre conceptos parecidos.
- Casos frontera de examen.
- Preguntas de aplicación, no solo memoria literal.
- Explicaciones completas tras fallo.
- Justificación de cada distractor.
- Reglas de oro, errores típicos y tips de examen.
- Tablas de apoyo en START, planes/DRP/autoprotección y valoración clínica TES.

## Archivos incluidos

| Archivo | Uso |
|---|---|
| TES_LEIXA_BANCO_COMPLETO_ASESOR_v805_AMPLIADO.csv | Banco completo original + nuevas preguntas. |
| TES_LEIXA_MATERIAL_DIDACTICO_ASESOR_v805_AMPLIADO.csv | Vista didáctica ampliada con nuevas explicaciones. |
| TES_LEIXA_PREGUNTAS_ASESOR_v805_AMPLIADO.jsonl | Banco completo ampliado, una pregunta por línea. |
| TES_LEIXA_COBERTURA_ASESOR_v805_AMPLIADO.csv | Cobertura recalculada tras ampliación. |
| TES_LEIXA_CONTROL_CALIDAD_ASESOR_v805_AMPLIADO.csv | Incidencias originales conservadas para revisión. |
| TES_LEIXA_RESUMEN_ESTRUCTURAL_v805_AMPLIADO.json | Resumen estructural actualizado. |
| TES_LEIXA_DEVOLUCION_ASESOR_CAMBIOS_AMPLIACION_v805.csv | Cambios en formato importable por el creador. |

## Advertencia de verificación oficial

Las nuevas preguntas son docentes y están pensadas para preparación de examen TES, pero cualquier literalidad normativa, criterio autonómico o requisito concreto de convocatoria debe contrastarse con el temario oficial vigente del centro/convocatoria.

## Recomendación técnica para la app

Importar las preguntas nuevas como registros añadidos, no como sustitución destructiva. Los IDs empiezan por `V805-LOG`, `V805-PLA` y `V805-ANA`, por lo que no colisionan con los IDs existentes.

Para evitar bucles y repetición:

1. No repetir la misma pregunta hasta que hayan aparecido al menos 20-30 preguntas distintas.
2. Penalizar repetición por `conceptos_clave` y no solo por `id`.
3. En modo práctica, mostrar explicación completa al fallar y breve al acertar.
4. En modo examen, ocultar explicación hasta terminar el bloque.
5. Desactivar avance automático tras fallo.
6. Reforzar temas fallados con prioridad, pero alternando subtema y dificultad.
7. Registrar estadísticas por módulo, tema, subtema y tipo de error.

## Resumen para el creador

### Archivos/carpetas actualizados
- Banco completo CSV ampliado.
- Material didáctico CSV ampliado.
- JSONL ampliado.
- Cobertura recalculada.
- Resumen estructural actualizado.
- CSV de cambios de ampliación.

### Cambios docentes
- Añadidas preguntas nuevas con 4 opciones homogéneas, una respuesta correcta, explicación, distractores justificados, regla de oro, error típico y mini-lección.

### Cambios técnicos recomendados
- Importar como altas nuevas, sin tocar usuarios/progreso/login/guardado.
- Usar `conceptos_clave` para evitar repetición semántica.

### Verificaciones pendientes
- Revisión oficial de literalidad normativa o criterios autonómicos si el temario de convocatoria lo exige.
