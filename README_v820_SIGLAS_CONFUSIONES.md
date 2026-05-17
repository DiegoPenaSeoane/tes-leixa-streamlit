# TES Leixa v8.20 — Siglas desplegadas + repaso por confusiones

Versión basada en v819. Mantiene el banco de 10.713 preguntas y añade una capa didáctica sobre siglas, confusiones y repaso dirigido.

## Cambios principales

- Diccionario global de siglas en la app.
- Si fallas una pregunta con siglas, la corrección muestra qué significa cada una.
- Registro de `familia_confusion` y `confusion_objetivo` en cada intento.
- Panel **Mis confusiones frecuentes**.
- Nuevo modo **Entrenar trampas/siglas**.
- Tratamiento especial de PMA, porque puede aparecer como Puesto Médico Avanzado o Puesto de Mando Avanzado según el contexto.

## Subida a GitHub

Sube a la raíz del repositorio:

```text
app.py
requirements.txt
README_v820_SIGLAS_CONFUSIONES.md
CHANGELOG_v820_SIGLAS_CONFUSIONES.md
docs/
scripts/
```

No reemplaces `user_store.json` ni `user_store (2).json`.

Después: Streamlit → Manage app → Clear cache → Reboot app.
