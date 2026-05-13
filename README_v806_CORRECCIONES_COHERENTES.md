# TES Leixa v8.06 — Correcciones coherentes por concepto

## Qué corrige

La v8.05 había saneado campos vacíos, pero podía conservar material incoherente si una pregunta tenía una tabla o regla asignada de otra familia conceptual.

Ejemplo corregido:
- Pregunta sobre lesión medular torácica.
- Antes: tabla de huesos + regla de comunicación.
- Ahora: tabla de lesiones medulares por nivel + regla neurológica específica.

## Validación

- Preguntas: 3413
- Respuestas inválidas: 0
- IDs duplicados: 0
- Filas medulares/neurológicas corregidas: 205
- Tablas genéricas mal asignadas corregidas: 34
- Mismatches medulares restantes: 0

## Qué mejora

- Lesión cervical vs torácica vs lumbar/conos/cauda equina.
- Diferencia con lesión cortical unilateral.
- Diferencia con plexo braquial.
- Regla específica: brazos conservados + ambas piernas afectadas = torácica/inferior; brazos afectados + piernas afectadas = cervical.
- La app prioriza tabla dinámica coherente si detecta pregunta medular.

## Subir a GitHub

Sube:

- app.py
- requirements.txt
- README_v806_CORRECCIONES_COHERENTES.md

Opcional:
- TES_LEIXA_BANCO_v806_CORRECCIONES_COHERENTES.csv
- INFORME_v806_CORRECCIONES_COHERENTES.json

## Debe aparecer

`Banco v8.06 · correcciones coherentes por concepto`
