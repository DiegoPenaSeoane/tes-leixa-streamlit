# TES LEIXA v8.19 — Supuestos prácticos: evacuación, sectorización y comunicaciones

Versión preparada para GitHub Web.

## Resultado

- Banco total: **10713 preguntas**.
- Se preserva el banco v8.18 y se sustituye el bloque repetitivo de Comunicaciones por preguntas nuevas de microfamilia.
- Se añaden **900 preguntas nuevas** basadas en supuestos prácticos de norias de evacuación, sectorización, riesgos NRBQ, PCAMB/PME/PMA, triaje, comunicaciones y protocolo radio.
- Filtros por asignatura, tema y subtema conservados.
- Banco embebido en `app.py`; no se suben CSV gigantes.

## Distribución

| modulo                       |   count |
|:-----------------------------|--------:|
| MP0061 Anatomofisiología     |    4570 |
| MP0053 Logística sanitaria   |    3484 |
| MP0059 Planes de emergencias |    2659 |

## Subida

Arrastra a la raíz del repositorio:

```text
app.py
requirements.txt
README_v819_SUPUESTOS_EVACUACION.md
CHANGELOG_v819_SUPUESTOS_EVACUACION.md
docs/
scripts/
```

No reemplaces `user_store.json` ni `user_store (2).json`.

Después: Streamlit → Manage app → Clear cache → Reboot app.
