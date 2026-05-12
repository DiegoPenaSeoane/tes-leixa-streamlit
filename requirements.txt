# TES Leixa v7.07 — PAQUETE COMPLETO PARA EL REPO CORRECTO

## REPOSITORIO CORRECTO

Subir estos archivos SOLO a:

`DiegoPenaSeoane/tes-leixa-streamlit`

NO subirlos a:

`drive-backend`

## Qué incluye

- Banco completo: 3407 preguntas.
- App final con:
  - plan 12+12
  - usuarios persistentes
  - modo Plan de hoy
  - Solo no respondidas
  - Solo mis fallos
  - Dificultad alta/filtro_10
  - aciertos sin repaso largo
  - fallos con aprendizaje completo
  - tablas, reglas, mnemotecnias y explicación profunda en fallos
- Requirements corregido para Streamlit Cloud.
- Docs y scripts de validación.

## Validación

- Preguntas: 3407
- Respuestas inválidas: 0
- IDs duplicados: 0

## Archivos a subir a GitHub

Sube todo esto al repositorio `tes-leixa-streamlit`:

- app.py
- requirements.txt
- data/
- docs/
- scripts/
- README_UPDATE_v707_TODO_REPO_CORRECTO.md

## Importante sobre usuarios/progreso

Este paquete NO incluye:

`data/user_store.json`

Eso es intencionado para no borrar usuarios, contraseñas ni progreso.

La persistencia real se activa con Streamlit Secrets:

```toml
GITHUB_TOKEN = "TU_TOKEN_NUEVO"
GITHUB_REPO = "DiegoPenaSeoane/tes-leixa-streamlit"
GITHUB_BRANCH = "main"
GITHUB_STORE_PATH = "data/user_store.json"
```

## Cómo comprobar que subiste al repo correcto

En GitHub la URL debe empezar por:

`https://github.com/DiegoPenaSeoane/tes-leixa-streamlit/`

NO por:

`https://github.com/DiegoPenaSeoane/drive-backend/`

## Después de subir

1. Commit changes.
2. Streamlit → Reboot app.
3. Ctrl + F5.
4. En la app debe aparecer:

`Banco v7.07 · paquete completo repo correcto.`
