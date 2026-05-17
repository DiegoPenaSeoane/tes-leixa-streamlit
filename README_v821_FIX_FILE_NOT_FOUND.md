# TES Leixa v8.21 — FIX FileNotFound Streamlit

Esta versión corrige el error `FileNotFoundError` provocado por un `app.py` equivocado o incompleto que intentaba leer un archivo externo con `Path(...).read_text()`.

## Qué incluye

- `app.py` completo y funcional.
- Banco v8.20 preservado: 10.713 preguntas.
- Mejoras v819 incluidas: supuestos de evacuación, sectorización y comunicaciones.
- Mejoras v820 incluidas: siglas desplegadas, confusiones frecuentes y modo trampas/siglas.
- El banco va embebido dentro de `app.py`, sin depender de CSV externo.

## Qué subir a GitHub

Sube/reemplaza SOLO estos archivos/carpetas desde este paquete:

```text
app.py
requirements.txt
README_v821_FIX_FILE_NOT_FOUND.md
CHANGELOG_v821_FIX_FILE_NOT_FOUND.md
docs/
scripts/
```

## Qué NO reemplazar

```text
user_store.json
user_store (2).json
```

## Después de subir

En Streamlit Cloud:

```text
Manage app → Clear cache → Reboot app
```

Debe aparecer:

```text
Banco v8.21 · 10713 preguntas · FIX FileNotFound · siglas + confusiones
```

## Nota importante

El error anterior mostraba algo parecido a:

```text
File "/mount/src/tes-leixa-streamlit/app.py", line 6
text = app.read_text(encoding="utf-8")
```

Eso significa que el `app.py` subido al repo NO era la app final, sino un archivo/parche equivocado. Este paquete reemplaza el `app.py` entero.
