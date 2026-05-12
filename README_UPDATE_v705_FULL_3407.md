# TES Leixa v7.05 — Paquete completo 3407

## Problema que corrige

Si la app muestra 3049 preguntas, significa que no se subió el banco nuevo de `data/`.

Este paquete incluye TODO lo necesario para que cargue el banco final:

- `app.py` con lógica v7.04: aciertos sin repaso largo, fallos con aprendizaje completo.
- `requirements.txt` mínimo.
- `data/tes_leixa_banco_v653_streamlit_ready.csv.gz` con 3407 preguntas.

## Validación

- Preguntas: 3407
- Respuestas inválidas: 0
- IDs duplicados: 0

## Subir a GitHub

Sube:

- app.py
- requirements.txt
- data/
- docs/
- scripts/
- README_UPDATE_v705_FULL_3407.md

## Importante sobre usuarios/progreso

Este paquete NO incluye `data/user_store.json`.

Eso es intencionado para no borrar usuarios ni progreso.

Pero para que el progreso persista de verdad en Streamlit Cloud necesitas configurar Secrets:

```toml
GITHUB_TOKEN = "TU_TOKEN"
GITHUB_REPO = "diegopenaseoane/tes-leixa-streamlit"
GITHUB_BRANCH = "main"
GITHUB_STORE_PATH = "data/user_store.json"
```

Si no lo configuras, la app puede funcionar, pero las sesiones se guardan solo de forma temporal.

## Después

- Commit changes
- Streamlit → Reboot app
- Ctrl + F5
