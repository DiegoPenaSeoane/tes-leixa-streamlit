# TES Leixa v8.00 — Archivo único blindado

## Por qué este enfoque

Para cortar los problemas de carpetas, rutas, CSV en raíz/data y parches acumulados:

- el banco de 3407 preguntas va incrustado dentro de `app.py`
- no depende de `data/`
- no depende de `tes_leixa_banco_v653_streamlit_ready.csv.gz`
- el guardado local usa `user_store.json`
- los fallos muestran explicación inmediatamente

## Validación

- Preguntas: 3407
- Respuestas inválidas: 0
- IDs duplicados: 0

## Usuarios

- diego / tes2026 → administrador
- anton / 1234
- melisa / 1111
- elvira / 2222
- lucia / 3333

## Subir a GitHub

Borra o ignora todo lo anterior y sube solo:

- app.py
- requirements.txt
- README_v800_ARCHIVO_UNICO.md

## Qué debes ver

`Banco v8.00 · archivo único blindado`

## Importante

Sin GitHub Secrets, el guardado local puede perderse si Streamlit redeploya el contenedor.
Pero no necesitas Secrets para que funcione durante la sesión de uso normal.
