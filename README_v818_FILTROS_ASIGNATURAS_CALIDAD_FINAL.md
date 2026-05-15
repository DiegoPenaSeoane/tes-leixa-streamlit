# TES Leixa v8.18 — filtros por asignatura y bloques

Versión lista para GitHub Web.

## Cambios principales

- Mantiene el banco de 9813 preguntas embebido en `app.py`.
- Añade filtro de estudio por asignatura: todo junto o elegir una/varias asignaturas.
- Añade filtro por tema/bloque y subtema/subbloque.
- Añade tabla de distribución del filtro activo.
- Mejora la cola para alternar asignaturas, temas y subtemas cuando estudias todo junto.
- Conserva usuarios y progreso: no subas ni reemplaces `user_store.json`.

## Cómo subir

Arrastra a la raíz del repo:

```text
app.py
requirements.txt
README_v818_FILTROS_ASIGNATURAS_CALIDAD_FINAL.md
CHANGELOG_v818_FILTROS_ASIGNATURAS_CALIDAD_FINAL.md
docs/
scripts/
```

No reemplaces:

```text
user_store.json
user_store (2).json
```

Después en Streamlit: `Manage app → Clear cache → Reboot app`.

Debe marcar: `Banco v8.18 FINAL · 9813 preguntas`.
