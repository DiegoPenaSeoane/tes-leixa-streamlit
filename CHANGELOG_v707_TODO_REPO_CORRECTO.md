# TES Leixa v7.01 — Banco expandido y estudio 12+12

Fecha: 2026-05-12 19:31

## Banco

- Preguntas nuevas de v701: 300
- Total final: 3407
- Respuestas inválidas: 0
- Duplicados corregidos: 0

## Conserva usuarios y progreso

Este paquete **NO incluye `data/user_store.json`**.  
Así no sobrescribe usuarios, contraseñas ni progreso si ya existen.

La app mantiene fallback con usuarios iniciales si no existe almacén:

- diego / tes2026 → administrador
- anton / 1234 → usuario
- melisa / 1111 → usuario
- elvira / 2222 → usuario
- lucia / 3333 → usuario

## Estudio 12 + 12

La app añade:

- plan de primera vuelta en 12 días
- plan de segunda vuelta en otros 12 días
- objetivo diario automático
- modo “Plan de hoy”
- modo “Solo no respondidas”
- modo “Solo mis fallos”
- modo “Dificultad alta/filtro_10”
- estadísticas por módulo
- subtemas débiles
- aprendizaje profundo si fallas
- refuerzo rápido si aciertas

## Correcciones técnicas incluidas

- requirements estables
- arranque seguro: login antes de cargar banco
- fallback de user_store
- fix `st.success/st.error`
- tabla/resumen específico mostrado desde CSV y por detección de concepto
