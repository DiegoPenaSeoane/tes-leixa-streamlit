# BRIEFING PARA ASESOR — Optimización TES Leixa v804

## Objetivo

Este paquete contiene el banco actual completo para que un asesor pueda optimizar la aplicación de estudio TES Leixa:
preguntas, opciones, respuesta correcta, explicaciones, porqués de distractores, reglas de oro, errores típicos,
tips de examen, minilecciones, mnemotecnias, tablas y campos de cobertura.

## Estado del banco exportado

- Total preguntas incluidas: **3413**
- Respuestas inválidas detectadas: **0**
- IDs duplicados detectados: **0**
- Incidencias potenciales para revisar: **27**

## Archivos incluidos

| Archivo | Uso |
|---|---|
| `TES_LEIXA_BANCO_COMPLETO_ASESOR_v804.csv` | Banco completo con todas las columnas existentes. |
| `TES_LEIXA_MATERIAL_DIDACTICO_ASESOR_v804.csv` | Vista principal para revisión didáctica. |
| `TES_LEIXA_PREGUNTAS_ASESOR_v804.jsonl` | Una pregunta por línea para revisión con IA/automatización. |
| `TES_LEIXA_CONTROL_CALIDAD_ASESOR_v804.csv` | Posibles problemas detectados automáticamente. |
| `TES_LEIXA_COBERTURA_ASESOR_v804.csv` | Cobertura por módulo, tema, subtema y dificultad. |
| `TES_LEIXA_RESUMEN_ESTRUCTURAL_v804.json` | Resumen estructural del banco. |
| `PLANTILLA_DEVOLUCION_ASESOR_CAMBIOS_v804.csv` | Formato para devolver mejoras integrables. |

## Qué debe revisar el asesor

### 1. Preguntas que regalan la respuesta

Buscar:
- respuesta literal dentro del enunciado;
- pistas gramaticales;
- opción correcta más larga o más específica que las demás;
- distractores de otra familia conceptual.

### 2. Calidad de distractores

Cada distractor debe explicar:
- por qué parece plausible;
- cuándo sería correcto;
- por qué aquí no lo es.

Formato ideal:

> Esta opción sería válida si..., pero en este caso el dato diferencial es...

### 3. Explicaciones tras fallo

Cuando el alumno falla, la respuesta debe enseñar:
- la regla aplicable;
- el error típico;
- el razonamiento diferencial;
- una tabla o esquema si el concepto es memorizable;
- una mini-lección que permita no repetir el fallo.

### 4. Tablas y baremos obligatorios

Añadir o mejorar tablas cuando aparezcan:
- Glasgow;
- START;
- AVPU;
- XABCDE;
- RCP/DEA;
- FEFO/FIFO/cadena de frío;
- tipos de planes;
- DRP;
- PMA/PSA/CME;
- norias;
- anatomía topográfica;
- regiones abdominales;
- huesos/articulaciones;
- signos neurológicos;
- qSOFA/sepsis;
- Código Ictus;
- material sanitario crítico.

### 5. Cobertura y dificultad

Reforzar:
- subtemas con pocas preguntas;
- dificultad alta/filtro_10;
- casos frontera;
- preguntas de integración: logística + triaje + comunicación + evacuación;
- anatomía aplicada a signos clínicos y actuación TES.

## Cómo devolver los cambios

Usar el archivo:

`PLANTILLA_DEVOLUCION_ASESOR_CAMBIOS_v804.csv`

Columnas obligatorias:
- `id`
- `accion`
- `campo_modificado`
- `valor_nuevo`
- `motivo`
- `prioridad`
- `fuente`
- `observaciones_integracion`

## Reglas para crear nuevas preguntas

Cada pregunta nueva debe tener:

1. ID nuevo único.
2. Módulo, tema y subtema.
3. Nivel de dificultad.
4. Enunciado claro.
5. 4 opciones homogéneas.
6. 1 sola respuesta correcta.
7. Explicación específica.
8. Porqués de las 3 opciones incorrectas.
9. Regla de oro.
10. Error típico.
11. Tip de examen.
12. Minilección.
13. Mnemotecnia si aplica.
14. Tabla/resumen si el concepto lo requiere.
15. Fuente o referencia de origen.

## No tocar

El asesor no debe tocar:
- usuarios;
- contraseñas;
- progreso;
- lógica de Streamlit;
- estructura de login;
- guardado local.

Este paquete es solo para optimizar el banco y el material de aprendizaje.
