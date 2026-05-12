# TES Leixa v7.08 — REINSTALACIÓN COMPLETA LIMPIA

Este paquete es para empezar limpio en el repositorio correcto:

`DiegoPenaSeoane/tes-leixa-streamlit`

## Incluye TODO

- `app.py`
- `requirements.txt` correcto
- `data/tes_leixa_banco_v653_streamlit_ready.csv.gz`
- `data/user_store.json`
- `docs/`
- `scripts/`
- este README

## Validación del banco

- Preguntas: 3407
- Respuestas inválidas: 0
- IDs duplicados: 0

## Usuarios incluidos

- diego / tes2026 → administrador
- anton / 1234 → usuario
- melisa / 1111 → usuario
- elvira / 2222 → usuario
- lucia / 3333 → usuario

## Qué hace la app

- Banco completo de 3407 preguntas.
- Plan de estudio 12 + 12 días.
- Aciertos sin repaso largo.
- Fallos con aprendizaje completo.
- Solo mis fallos.
- Solo no respondidas.
- Dificultad alta/filtro_10.
- Tablas, reglas, mnemotecnias y explicación profunda en fallos.
- Persistencia por usuario mediante `data/user_store.json`.

## FORMA SIMPLE DE SUBIR

En GitHub, dentro del repositorio `tes-leixa-streamlit`:

1. Borra o reemplaza los archivos antiguos si hace falta.
2. Sube TODO el contenido de este ZIP a la raíz del repo.
3. Asegúrate de que quede así:

```text
tes-leixa-streamlit/
  app.py
  requirements.txt
  data/
    tes_leixa_banco_v653_streamlit_ready.csv.gz
    user_store.json
  docs/
  scripts/
  README_REINSTALACION_COMPLETA_v708.md
```

## requirements.txt correcto

El archivo `requirements.txt` debe contener SOLO:

```txt
pandas==2.2.2
numpy==1.26.4
openpyxl==3.1.5
rich==13.9.4
markdown-it-py==3.0.0
mdurl==0.1.2
pygments==2.19.2
```

## Streamlit Secrets

En Streamlit → Manage app → Settings → Secrets:

```toml
GITHUB_TOKEN = "TU_TOKEN_NUEVO"
GITHUB_REPO = "DiegoPenaSeoane/tes-leixa-streamlit"
GITHUB_BRANCH = "main"
GITHUB_STORE_PATH = "data/user_store.json"
```

## Después de subir

1. Commit changes.
2. Streamlit → Reboot app.
3. Ctrl + F5.

Debe aparecer:

`Banco v7.08 · reinstalación completa limpia.`
